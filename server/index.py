
from flask import Flask, request, jsonify # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy import exc # type: ignore
from flask_cors import CORS # type: ignore
from dotenv import load_dotenv # type: ignore
import os
import uuid
load_dotenv()


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/smartstudy_db'

# Configure MySQL connection
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database_name'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Configure dotenv
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/smartstudy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It's a good practice to disable this unless needed

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    firstName = db.Column(db.String(80), unique=True, nullable=False)
    lastName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)  # Ensure email is unique
    password = db.Column(db.String(80), nullable=False)
    cpassword = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.firstName

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Course %r>' % self.course_name

# Create all tables if they do not exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Welcome to Smart Study Application, designed to help primary students access digital education.'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    cpassword = data.get('cpassword')
    if password != cpassword:
        return jsonify({'message': 'Passwords do not match'}), 400
    try:
        new_user = User(firstName=firstName, lastName=lastName, email=email, password=password, cpassword=cpassword)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully', 'redirect_url': './login.html'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Username or email already exists'}), 409

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    firstName = data.get('firstName')
    password = data.get('password')
    user = User.query.filter_by(firstName=firstName, password=password).first()
    if user:
        return jsonify({'message': 'Login successful', 'redirect_url': './dashboard.html'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.get_json()
    course_name = data.get('courseName')
    category = data.get('category')
    level = data.get('level')
    try:
        new_course = Course(course_name=course_name, category=category, level=level)
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Course added successfully"})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Course already exists'}), 409

@app.route('/get_courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    course_list = [{'id': course.id, 'courseName': course.course_name, 'category': course.category, 'level': course.level} for course in courses]
    return jsonify(course_list)

if __name__ == '__main__':
    app.run(debug=True, port=7000)

  
  
  #message

# Define Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(250), nullable=False)

    # Create all tables if they do not exist
with app.app_context():
    db.create_all()
    

# Routes
#api to create all messages
@app.route('/messages', methods=['POST'])
def send_message():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')
        new_message = Message(name=name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        return jsonify(message="Your Message has been sent successfully", sentMessage={'id': new_message.id, 'name': new_message.name, 'email': new_message.email, 'subject': new_message.subject, 'message': new_message.message}), 201
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500
    
#api to get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    try:

        all_messages = Message.query.all()
        if not all_messages:
            return jsonify(message="No messages found!"), 404
        else:
            messages = [{ 'id': message.id, 'name': message.name, 'email': message.email, 'subject': message.subject,'message': message.message} for message in all_messages]
            return jsonify(message="These are my messages", allMessages=messages), 200
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500


@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        delete_message = Message.query.get(message_id)
        if not delete_message:
            return jsonify(message="Message not found"), 404
        else:
            db.session.delete(delete_message)
            db.session.commit()
            return jsonify(message="Message deleted successfully"), 200
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port = 7000)

