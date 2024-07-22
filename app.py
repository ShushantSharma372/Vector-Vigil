from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Define the User model
class ValidateInfo(db.Model):
    __tablename__ = 'validationinfo'
    UserID = db.Column(db.String(255), primary_key=True)
    EmployeeName = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    MedicalInstitutionName = db.Column(db.String(255), nullable=False)
    MedicalInstitutionID = db.Column(db.String(255), nullable=False)

# Define the Query model
class Query(db.Model):
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20), nullable=False)
    query = db.Column(db.String(500), nullable=False)

    def __init__(self, name, number, query):
        self.name = name
        self.number = number
        self.query = query

# Define the Alert model
class Alert(db.Model):
    __tablename__ = 'alertformsubmissions'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    mobileNo = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    submissionDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)

    def __init__(self, firstName, lastName, email, mobileNo, region):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.mobileNo = mobileNo
        self.region = region

# Define the LogCase model
class MedicalUserInfo(db.Model):
    __tablename__ = 'medicaluserinfo'
    UserID = db.Column(db.String(255), primary_key=True)
    MedicalInstitutionID = db.Column(db.String(255), nullable=False)
    Region = db.Column(db.String(255), nullable=False)
    NumberOfCases = db.Column(db.Integer, nullable=False)
    submissionDate = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        message = request.form['message']

        new_query = Query(name=name, number=phone, query=message)
        try:
            db.session.add(new_query)
            db.session.commit()
            message = "Message Recieved."
        except Exception as e:
            db.session.rollback()
            message = f"Error: {e}"

    return render_template('index.html', message=message)

@app.route('/alerts', methods=['GET', 'POST'])
def alert():
    message = None
    print(f"Request method: {request.method}")
    print(f"Request form: {request.form}")
    print(f"Request data: {request.data}")
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.get_json()
        else:
            data = request.form

        print(f"Processed data: {data}")
        
        try:
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            mobile_no = data.get('website')
            region = data.get('region')

            print(f"first_name: {first_name}, last_name: {last_name}, email: {email}, mobile_no: {mobile_no}, region: {region}")

            new_alert = Alert(firstName=first_name, lastName=last_name, email=email, mobileNo=mobile_no, region=region)
            db.session.add(new_alert)
            db.session.commit()
            return jsonify({"message": "Form submitted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {e}"}), 500

    return render_template('alerts.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/log_info', methods=['GET', 'POST'])
def log_info():
    if request.method == 'POST':
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')

        user = ValidateInfo.query.filter_by(UserID=username).first()
        
        if user:
            if user.Password == password:
                new_case = MedicalUserInfo(
                    UserID=username,
                    MedicalInstitutionID=user.MedicalInstitutionID,
                    Region=data.get('region'),
                    NumberOfCases=data.get('cases')
                )
                try:
                    db.session.add(new_case)
                    db.session.commit()
                    return jsonify({"message": "Form submitted successfully!"}), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"message": f"Error: {e}"}), 500
            else:
                return jsonify({"message": "Invalid password!"}), 401
        else:
            return jsonify({"message": "User does not exist!"}), 401
    
    return render_template('log_info.html')

if __name__ == '__main__':
    app.run(debug=True)
