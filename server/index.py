from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/smartstudy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # It's a good practice to disable this unless needed
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
