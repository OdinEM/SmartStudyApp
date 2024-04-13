from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/smartstudy_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=True, nullable=False)
    lastName = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cpassword = db.Column(db.String(80), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.firstName

# Create all tables if they do not exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Welcome to smart study application, an application designed to help primary students to have access to digital education'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    cpassword = data.get('cpassword')
    try:
        new_user = User(firstName=firstName,lastName=lastName, email=email, password=password, cpassword=cpassword)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully',  'redirect_url': '/login.html'})
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'firstName already exists'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    firstName = data.get('firstName')
    password = data.get('password')
    user = User.query.filter_by(firstName=firstName, password=password).first()
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'})

if __name__ == '__main__':
    app.run(debug=True, port=7000)

