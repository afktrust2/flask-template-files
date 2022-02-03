from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "user_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print (results[0])
        return cls(results[0])

    @staticmethod
    def validate_register(users):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, users)
        if len(results) >= 1:
            flash("Email already in use.","register")
            is_valid=False
        if not EMAIL_REGEX.match(users['email']):
            flash("Invalid Email!","register")
            is_valid=False
        if len(users['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(users['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(users['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if users['password'] != users['confirm']:
            flash("Passwords don't match","register")
        return is_valid