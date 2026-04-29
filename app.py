from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import date

app = Flask(__name__)

#Database Connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='pet_adoption'
    )
    return connection

#Search Pets by Breed and/or Species
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        species = request.form.get('species', '').strip()
        breed = request.form.get('breed', '').strip()
    else:
        species = request.args.get('species', '').strip()
        breed = request.args.get('breed', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
 
    query = "SELECT * FROM Pet WHERE 1=1"
    params = []

    if species:
        query += " AND species LIKE %s"
        params.append(f"%{species}%")

    if breed:
        query += " AND breed LIKE %s"
        params.append(f"%{breed}%")

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'search_results.html',
        pets=results,
        species=species,
        breed=breed
    )

#Home Page
@app.route('/')
def home():
    return render_template('home.html')

#View All Pets
@app.route('/pets')
def pets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Pet")
    pets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pets.html', pets=pets)


#Pet Details
@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Pet WHERE pet_id = %s", (pet_id,))
    pet = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('petdetails.html', pet=pet)


#Adoption Application
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        #adopter_id = request.form['adopter_id']
        adopter_name = request.form['adopter_name']
        age = request.form['age']
        email = request.form['email']
        pet_id = request.form['pet_id']
        #application_id = request.form['application_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        #Insert adopter
        cursor.execute(
            """
            INSERT INTO Adopter (adopter_name, email, age)
            VALUES (%s, %s, %s)
            """,
            (adopter_name, email, age)
        )
        adopter_id= cursor.lastrowid

        #Insert application
        cursor.execute(
            """
            INSERT INTO AdoptionApplication (application_date, application_status, pet_id)
            VALUES (%s, %s, %s)
            """,
            ( date.today(), 'Pending', pet_id)
        )
        application_id= cursor.lastrowid

        #Link adopter to application
        cursor.execute(
            """
            INSERT INTO Submits (application_id, adopter_id)
            VALUES (%s, %s)
            """,
            (application_id, adopter_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('pets'))

    pet_id = request.args.get('pet_id')
    return render_template('apply.html', pet_id=pet_id)


#Admin Dashboard
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT aa.application_id, aa.application_date, aa.application_status,
               p.pet_name,
               a.adopter_name, a.email
        FROM AdoptionApplication aa
        JOIN Pet p ON aa.pet_id = p.pet_id
        JOIN Submits s ON aa.application_id = s.application_id
        JOIN Adopter a ON s.adopter_id = a.adopter_id
    """)
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin.html', applications=applications)

#Reports / Aggregate Query
@app.route('/reports')
def reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT application_status, COUNT(*) AS total_applications
        FROM AdoptionApplication
        GROUP BY application_status
    """)

    status_counts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('reports.html', status_counts=status_counts)


#Approve Application
@app.route('/approve/<int:app_id>')
def approve(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE AdoptionApplication SET application_status = 'Approved' WHERE application_id = %s",
        (app_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))


#Reject Application
@app.route('/reject/<int:app_id>')
def reject(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE AdoptionApplication SET application_status = 'Rejected' WHERE application_id = %s",
        (app_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))

#Delete Application
@app.route('/delete_application/<int:app_id>')
def delete_application(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete from relationship tables first because of foreign keys
    cursor.execute(
        "DELETE FROM Reviews WHERE application_id = %s",
        (app_id,)
    )

    cursor.execute(
        "DELETE FROM Submits WHERE application_id = %s",
        (app_id,)
    )

    # Then delete the actual application
    cursor.execute(
        "DELETE FROM AdoptionApplication WHERE application_id = %s",
        (app_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))

#Match Compatibility of Applicant with Available Pets
@app.route('/matches')
def matches():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM vw_match_scores v
        WHERE match_score = (
            SELECT MAX(match_score)
            FROM vw_match_scores
            WHERE pet_id = v.pet_id
        )
        ORDER BY pet_id
    """)

    matches = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('matches.html', matches=matches)

#Run App
if __name__ == '__main__':
    app.run(debug=True)
