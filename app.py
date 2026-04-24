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

    return render_template('pet_details.html', pet=pet)


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


#Run App
if __name__ == '__main__':
    app.run(debug=True)