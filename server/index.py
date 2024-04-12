# app.py
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="smartstudy"
)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    cursor = db.cursor()
    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    val = (data['username'], data['email'], data['password'])
    cursor.execute(sql, val)
    db.commit()
    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
