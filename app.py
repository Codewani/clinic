from flask import Flask, render_template, request, redirect, session
from flask_session import Session

from flask_mysqldb import MySQL

app = Flask(__name__)

f = open("C:\\Users\hp elitebook\password.txt", "r")
password = f.read()
f.close()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = "hospital"
#The line below ensures that the fetchall function returns a dictionary instead of a list
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = MySQL(app)

#A function that allows me to open the mySQL cursor, execute a command(INSERT, DELETE or UPDATE) and commit the changes instead of repeating the same code
def execute(command, *args):
    #Command: could be "INSERT INTO table (field_1, field_2, field_3) VALUES (%s, %s, %s)"
    #args: is the data that is supposed to go into the place holders "%s".
    fields = list()
    for field in args:
        fields.append(field)
    cur = db.connection.cursor()
    #check if the fields list is empty
    if fields:
        cur.execute(command, fields)
    else:
        cur.execute(command)
    db.connection.commit()
    cur.close
#Allows me to fetch data from a query request.
def fetch(command, type):
    cur = db.connection.cursor()
    patients = cur.execute(command)
    data = cur.fetchall()
    cur.close
    if type == "all":
        return data
    return data[0]

@app.route("/")
def hello_world():
    return render_template("main.html")

@app.route("/ward", methods=['GET', 'POST'])
def ward():
    if request.method == 'POST':
        ward_id         = request.form['ward_id']
        ward_name       = request.form['ward_name']
        number_beds     = request.form['number_beds']
        nurse_in_charge = request.form['nurse_in_charge']
        ward_type       = request.form['ward_type']

        execute("INSERT INTO ward (ward_id, ward_name, number_beds, nurse_in_charge, ward_type) VALUES (%s, %s, %s, %s, %s)", ward_id, ward_name, number_beds, nurse_in_charge, ward_type)
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

        execute("INSERT INTO patient (patient_id, name, initials, sex, address, post_code, admission, DOB, ward_id_id, next_of_kin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", patient_id, name, initials, sex, address, post_code, admission, DOB, ward_id, next_of_kin)

    return render_template("patients.html")

@app.route("/viewPatients")
def viewPatients():
    patientDetails = fetch("SELECT * FROM patient", "all")
    return render_template('viewpatients.html', patients=patientDetails)

@app.route("/viewWards")
def viewWards():
    wardDetails = fetch("SELECT * FROM ward", "all")
    return render_template('viewward.html', wards=wardDetails)

@app.route("/editpatient/<string:patient_id>", methods=['GET', 'POST'])
def editpatient(patient_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM patient WHERE patient_id = %s", (patient_id, ))
    patient = cur.fetchone()
    cur.close
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
        
        execute("UPDATE patient SET name = %s, initials = %s, sex = %s, address = %s, post_code = %s, admission = %s, DOB = %s, ward_id_id = %s, next_of_kin = %s WHERE patient_id = %s", name, initials, sex, address, post_code, admission, DOB, ward_id, next_of_kin, patient_id)
        
        return redirect("/viewPatients")
    return render_template("editpatients.html", patient = patient)

@app.route("/editward/<string:ward_id>", methods=['GET', 'POST'])
def editward(ward_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM ward WHERE ward_id = %s", (ward_id, ))
    ward = cur.fetchone()
    cur.close
    if request.method == 'POST':
        ward_id         = request.form['ward_id']
        ward_name       = request.form['ward_name']
        number_beds     = request.form['number_beds']
        nurse_in_charge = request.form['nurse_in_charge']
        ward_type       = request.form['ward_type']

        execute("UPDATE ward SET ward_name = %s, number_beds = %s, nurse_in_charge = %s, ward_type = %s WHERE ward_id = %s", ward_name, number_beds, nurse_in_charge, ward_type, ward_id)
        return redirect("/viewWards")
    return render_template("editward.html", ward = ward)

@app.route("/deletepatient/<string:patient_id>", methods=['GET', 'POST'])
def deletepatient(patient_id):
    if request.method == 'POST':
        execute("DELETE from patient WHERE patient_id = %s", (patient_id, ))
        return redirect("/viewPatients")
    return render_template("delete_patient.html", patient_id = patient_id)

@app.route("/deleteward/<string:ward_id>", methods=['GET', 'POST'])
def deleteward(ward_id):
    if request.method == 'POST':
        execute("DELETE from ward WHERE ward_id = %s", (ward_id, ))
        return redirect("/viewWards")
    return render_template("delete_ward.html", ward_id = ward_id)

@app.route("/wardPatients/<string:ward_id>", methods=['GET'])
def wardPatients(ward_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * from patient WHERE ward_id_id = %s", (ward_id,))
    patients = cur.fetchall()
    cur.execute("SELECT ward_name from ward WHERE ward_id = %s", (ward_id,))
    ward_name = cur.fetchall()[0]['ward_name']

    return render_template("wardPatients.html", patients = patients, ward_name = ward_name)

@app.route("/register", methods = ["GET", "POST"])
def register():
    passwordError = False
    if request.method == 'POST':
        employee_id      = request.form['employee_id']
        FirstName        = request.form['FirstName']
        LastName         = request.form['LastName']
        sex              = request.form['sex']
        address          = request.form['address']
        post_code        = request.form['post_code']
        DOB              = request.form['DOB']
        email            = request.form['email']
        password         = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            passwordError = True
            return render_template("authenticate/register.html", passwordError = passwordError)

        execute("INSERT INTO users (employeeId, FirstName, LastName, sex, address, postCode, DOB, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", employee_id, FirstName, LastName, sex, address, post_code, DOB, email, password)
        return redirect("/login")
    return render_template("authenticate/register.html", passwordError = passwordError)
@app.route("/login")
def login():
    return render_template("authenticate/login.html")



