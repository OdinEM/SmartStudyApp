from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="smartstudy_db"
)

# Create table if not exists


# Call function to create table
create_table()



if __name__ == '__main__':
    app.run(debug=True, port=7000)
