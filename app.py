from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ==============================
# Database Connection
# ==============================

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='pet_adoption'
    )
    return connection


# ==============================
# Home Page
# ==============================
@app.route('/')
def home():
    return render_template('home.html')


# ==============================
# View All Pets
# ==============================
@app.route('/pets')
def pets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Pet")
    pets = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('pets.html', pets=pets)


# ==============================
# Pet Details
# ==============================
@app.route('/pets/<int:pet_id>')
def pet_details(pet_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Pet WHERE pet_id = %s", (pet_id,))
    pet = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('pet_details.html', pet=pet)


# ==============================
# Adoption Application
# ==============================
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        pet_id = request.form['pet_id']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO AdoptionApplication (name, email, phone, pet_id, status)
            VALUES (%s, %s, %s, %s, 'Pending')
            """,
            (name, email, phone, pet_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('pets'))

    pet_id = request.args.get('pet_id')
    return render_template('apply.html', pet_id=pet_id)


# ==============================
# Admin Dashboard
# ==============================
@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM AdoptionApplication")
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin.html', applications=applications)


# ==============================
# Approve Application
# ==============================
@app.route('/approve/<int:app_id>')
def approve(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE AdoptionApplication SET status='Approved' WHERE id=%s",
        (app_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))


# ==============================
# Reject Application
# ==============================
@app.route('/reject/<int:app_id>')
def reject(app_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE AdoptionApplication SET status='Rejected' WHERE id=%s",
        (app_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin'))


# ==============================
# Run App
# ==============================
if __name__ == '__main__':
    app.run(debug=True)
