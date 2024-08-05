from flask import Flask, redirect, url_for, render_template, request, session,flash,send_file
from flask_compress import Compress
from datetime import timedelta
from datetime import datetime
import base64 
from werkzeug.utils import secure_filename
import os
import psycopg2.extras
import psycopg2

app = Flask(__name__)
app.jinja_env.filters['b64encode'] =  base64.b64encode
Compress(app)
app.secret_key = "helloo"
app.permanent_session_lifetime = timedelta(days=5)
app.config['UPLOAD_FOLDER'] = 'static/profileImages'
app.debug = True
database_session = psycopg2.connect(
    database='hospital',
    port=5432,
    host='localhost',
    user='postgres',
    password='Aa01156228722'
)



cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute('SELECT email FROM patient WHERE email = %s AND password = %s', ("omar@gmail.com", "1111"))
result = cursor.fetchone()
print(result)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def register_patient():

    message = ''
    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    age=request.form.get('age')
    bloodtype = request.form.get('blood')

    if 'profile_picture' in request.files:
        profile_picture = request.files['profile_picture']
        
        if profile_picture.filename != '':
            # Secure the filename and create a unique filename with patient's name
            secure_name = secure_filename(username)
            file_extension = os.path.splitext(profile_picture.filename)[1]  # Get the file extension
            unique_filename = f'{secure_name}_{age}{file_extension}'  # Unique filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Ensure the upload folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            profile_picture.save(file_path)
            file_url = f'profileImages/{unique_filename}'  # Relative path for the file
        else:
            file_url = None
    else:
        file_url = None


    if email:
        cursor.execute('SELECT email FROM patient where email = %s', (email,))
        if cursor.fetchone():
            message = 'Account already exits!'
        else:
            cursor.execute('INSERT INTO patient(patient_name, email,age,blood_type, password,profile_picture) VALUES (%s, %s ,%s,%s,%s,%s)',
                           (username, email,age,bloodtype, password, file_url))
            database_session.commit()
            message = 'You have successfully registered'

    return render_template('signup.html')


@app.route('/surgery')
def redirect_to_surgery():
    return render_template('surgery.html')


@app.route('/dental')
def redirect_to_dental():
    return render_template('dental.html')


@app.route('/about')
def redirect_to_about():
    return render_template('about.html')


@app.route("/contactus", methods=["POST", "GET"])
def contactus():
    message = ''
    if request.method == "POST":  # Ensure it's a POST request
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phonenumber")
        complaint = request.form.get("message")
        if email:
            cursor.execute('SELECT email FROM patient')
            result = cursor.fetchall()
            print(result)
            if not(any(email == row[0] for row in result)):
                message='you do not have an account please signup' 
                return render_template('signup.html', msg=message)
            try:
                cursor.execute('INSERT INTO contactus(name, email, phonenumber, message) VALUES (%s, %s, %s, %s)',
                               (name, email, phone, complaint))
                message = 'You have successfully sent your complaint'
                database_session.commit()
            except Exception as e:
                database_session.rollback()  # Rollback the changes if an error occurs
                message = f'Error occurred: {str(e)}'
                # Print the error to the console for debugging
                print(f"Error occurred: {str(e)}")

            print(message)
            return render_template("contactus.html", msg=message)
        
    return render_template("contactus.html",msg = message)


@app.route('/drlogin', methods=["POST", "GET"])
def doctorlogin():
    message = ''
    email = request.form.get('email')
    password = request.form.get('password')
    if email:
        cursor.execute('SELECT doctor_ID,doctor_name,specialization,department_ID,doctor_email,doctor_image_path FROM doctor WHERE doctor_email = %s AND doctor_password = %s', (email, password))
        result = cursor.fetchone()
        if result:
            doctor_data = dict(result)
            session['Doctor'] = doctor_data
            cursor.execute('''
                SELECT reservation.day, reservation.hour, patient.patient_id, patient.patient_name
                FROM reservation
                JOIN patient ON reservation.patient_id = patient.patient_id
                WHERE reservation.doctor_id = %s
            ''', (doctor_data['doctor_id'],))

            appointments = cursor.fetchall()
            database_session.commit()
            return render_template('doctorprofile.html', doctor=doctor_data,appointments=appointments)
        else:
            message = 'Please enter correct email/password'
            return render_template('drlogin.html', msg=message)  # Return login template with the error message

    return render_template('drlogin.html', msg=message)




@app.route('/doctor_profile')
def doctor_profile():
    # Assume you have retrieved doctor data and appointments
    doctor_data = {"doctor_name": "Dr. Smith"}  # Replace with actual doctor data
    appointments = [
        {"day": "2024-01-02", "hour": "10am", "patient_id": "Patient B"},
        # Add more appointments as needed
    ]
    return render_template('drpro.html', doctor=doctor_data, appointments=appointments)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if "Patient" in session:
        Patient = session["Patient"]
        Patient['patient_name'] = request.form['patient_name']
        Patient['email'] = request.form['email']
        Patient['age'] = request.form['age']
        update_query = '''
            UPDATE patient
            SET patient_name = %s, email = %s, age = %s
            WHERE patient_id = %s
            '''

        values = (Patient['patient_name'] , Patient['email'], Patient['age'],Patient['patient_id'] )
        cursor.execute(update_query, values)

        cursor.execute('''
                SELECT reservation.day, reservation.hour, doctor.doctor_name
                FROM reservation
                JOIN doctor ON reservation.doctor_id = doctor.doctor_id
                WHERE reservation.patient_id = %s
            ''', (Patient['patient_id'],))
        appointments = cursor.fetchall()
        return render_template('profile.html', Patient=Patient,appointments=appointments)
    


@app.route('/submit', methods=["POST", "GET"])
def submit():
    message = ''
    if "Patient" in session:
        patient = session["Patient"]
    if "appointments" in session:
        appointments = session['appointments']

    if request.method == "POST":
        
        doctorID = request.form.get("doctor")
        date = request.form.get("date")
        time = request.form.get("time")


        # Convert the date string to a datetime object
        selected_date = datetime.strptime(date, '%Y-%m-%d')

        # Check if the selected date is in the past
        if selected_date < datetime.now():
            message = 'Date has passed. Please select a future date.'
            flash(message, category='error')
            return render_template('profile.html', msg=message, Patient=patient, appointments=appointments)

        cursor.execute('SELECT doctor_id FROM reservation WHERE hour = %s AND day = %s', (time, date))
        result = cursor.fetchall()
        
        if result is None:
            cursor.execute('INSERT INTO reservation(doctor_id, patient_id, day, hour) VALUES (%s, %s, %s, %s)',
                           (doctorID, patient['patient_id'], date, time))
            message = 'Done'
            database_session.commit()
            return redirect(url_for("update"))

        if any(doctorID == row[0] for row in result):
            message = 'Doctor is busy'

            cursor.execute('''
                SELECT reservation.day, reservation.hour, doctor.doctor_name
                FROM reservation
                JOIN doctor ON reservation.doctor_id = doctor.doctor_id
                WHERE reservation.patient_id = %s
            ''', (patient['patient_id'],))

            appointments = cursor.fetchall()
            return render_template('profile.html', msg=message, Patient=patient, appointments=appointments)

        
        else:
            cursor.execute('SELECT patient_id FROM reservation WHERE hour = %s AND day = %s', (time, date))
            result = cursor.fetchall()
            database_session.commit()
            if any(patient['patient_id'] == row[0] for row in result):
                message = 'You have an appointment with another doctor at the same time'
                cursor.execute('''
                SELECT reservation.day, reservation.hour, doctor.doctor_name
                FROM reservation
                JOIN doctor ON reservation.doctor_id = doctor.doctor_id
                WHERE reservation.patient_id = %s
            ''', (patient['patient_id'],))
                appointments = cursor.fetchall()
                return render_template('profile.html', msg=message, Patient=patient, appointments=appointments)
            else:
                cursor.execute('INSERT INTO reservation(doctor_id, patient_id, day, hour) VALUES (%s, %s, %s, %s)',
                               (doctorID, patient['patient_id'], date, time))
                message = 'Done'
                database_session.commit()
                return redirect(url_for("update"))

            
@app.route('/update', methods=['GET', 'POST'])
def update():
    patient = session["Patient"]
    cursor.execute('''
                SELECT reservation.day, reservation.hour, doctor.doctor_name
                FROM reservation
                JOIN doctor ON reservation.doctor_id = doctor.doctor_id
                WHERE reservation.patient_id = %s
            ''', (patient['patient_id'],))
    appointments = cursor.fetchall()
    return render_template('profile.html', msg="done", Patient=patient,appointments=appointments)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    email = request.form.get('email')
    password = request.form.get('password')
    if email:
        cursor.execute('SELECT patient_name,email,patient_id,blood_type,age,profile_picture FROM patient WHERE email = %s AND password = %s', (email, password))
        result = cursor.fetchone()
        cursor.execute('SELECT profile_picture FROM patient WHERE email = %s AND password = %s', (email, password))
        profile_picture = cursor.fetchone()
        if result:

            session.permanent = True
            patient_data = dict(result)
            session['Patient'] = patient_data
            cursor.execute('''
                SELECT reservation.day, reservation.hour, doctor.doctor_name
                FROM reservation
                JOIN doctor ON reservation.doctor_id = doctor.doctor_id
                WHERE reservation.patient_id = %s
            ''', (patient_data['patient_id'],))
            appointments = cursor.fetchall()
            session['appointments'] = appointments
            database_session.commit()

            return render_template('profile.html', Patient=patient_data,appointments=appointments)
        else:
            message = 'Please enter correct email/password'
            return render_template('signin.html', msg=message)  # Return login template with the error message

    return render_template('signin.html', msg=message)



@app.route("/logout")
def logout():
    session.pop("patient", None)
    return redirect(url_for("login"))
@app.route("/logoutdr")
def logoutdr():
    session.pop("Doctor", None)
    return redirect(url_for("doctorlogin"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
