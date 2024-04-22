from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "Wongani1234@"
app.config['MYSQL_DB'] = "hospital"
#The line below ensures that the fetchall function returns a dictionary instead of a list
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)

@app.route("/")
def hello_world():
    return render_template("main.html")

@app.route("/ward")
def ward():
    if request.method == 'POST':
        ward_id         = request.form['ward_id']
        ward_name       = request.form['ward_name']
        number_beds     = request.form['number_beds']
        nurse_in_charge = request.form['nurse_in_charge']
        ward_type       = request.form['ward_type']

        cur = db.connection.cursor()

        cur.execute("INSERT INTO ward (ward_id, ward_name, number_beds, nurse_in_charge, ward_type) VALUES (%s, %s, %s, %s)", (ward_id, ward_name, number_beds, nurse_in_charge, ward_type))
        db.connection.commit()
        cur.close
    return render_template("ward.html")

@app.route("/patients", methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        patient_id  = request.form['patient_id']
        name        = request.form['name']
        initials    = request.form['initials']
        sex         = request.form['sex']
        address     = request.form['address']
        post_code   = request.form['post_code']
        admission   = request.form['admission']
        DOB         = request.form['DOB']
        ward_id     = request.form['ward_id']
        next_of_kin = request.form['next_of_kin']

        cur = db.connection.cursor()

        cur.execute("INSERT INTO patient (patient_id, name, initials, sex, address, post_code, admission, DOB, ward_id_id, next_of_kin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (patient_id, name, initials, sex, address, post_code, admission, DOB, ward_id, next_of_kin))
        db.connection.commit()
        cur.close
    return render_template("patients.html")

@app.route("/viewPatients")
def viewPatients():
    cur = db.connection.cursor()
    patients = cur.execute("SELECT * FROM patient")
    
    if patients > 0:
        patientDetails = cur.fetchall()
        return render_template('viewpatients.html', patients=patientDetails)

@app.route("/viewWards")
def viewWards():
    cur = db.connection.cursor()
    wards = cur.execute("SELECT * FROM ward")
    
    if wards > 0:
        wardDetails = cur.fetchall()
        return render_template('viewward.html', wards=wardDetails)

@app.route("/editpatient/<string:patient_id>", methods=['GET', 'POST'])
def editpatient(patient_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id, ))
    patients = cur.fetchall()
    patient = patients[0]
    if request.method == 'POST':
        patient_id  = request.form['patient_id']
        name        = request.form['name']
        initials    = request.form['initials']
        sex         = request.form['sex']
        address     = request.form['address']
        post_code   = request.form['post_code']
        admission   = request.form['admission']
        DOB         = request.form['DOB']
        ward_id     = request.form['ward_id']
        next_of_kin = request.form['next_of_kin']
        cur.execute("UPDATE patient SET name = %s, initials = %s, sex = %s, address = %s, post_code = %s, admission = %s, DOB = %s, ward_id_id = %s, next_of_kin = %s WHERE patient_id = %s", (name, initials, sex, address, post_code, admission, DOB, ward_id, next_of_kin, patient_id))
        db.connection.commit()
        cur.close
        return redirect("/viewPatients")
    return render_template("editpatients.html", patient = patient)

@app.route("/editward/<string:ward_id>", methods=['GET', 'POST'])
def editward(ward_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM ward WHERE ward_id = %s", (ward_id, ))
    wards = cur.fetchall()
    ward = wards[0]
    if request.method == 'POST':
        ward_id         = request.form['ward_id']
        ward_name       = request.form['ward_name']
        number_beds     = request.form['number_beds']
        nurse_in_charge = request.form['nurse_in_charge']
        ward_type       = request.form['ward_type']

        cur.execute("UPDATE ward SET ward_name = %s, number_beds = %s, nurse_in_charge = %s, ward_type = %s WHERE ward_id = %s", (ward_name, number_beds, nurse_in_charge, ward_type, ward_id))
        db.connection.commit()
        cur.close
        return redirect("/viewWards")
    return render_template("editward.html", ward = ward)

    
@app.route("/login")
def login():
    return render_template("authenticate/login.html")


