from sasquatch_app.config.mysqlconnection import connectToMySQL
from flask import flash


import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("First Name must be at least 2 characters","first_name")
            is_valid = False

        if len(form_data['last_name']) < 2:
            flash("Last Name must be at least 2 characters","last_name")
            is_valid = False

        if not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid Email address","email")
            is_valid = False

        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters","password")
            is_valid = False

        if form_data['password'] !=  form_data['confirm_p']:
            flash("Passwords do not match!","confirm_p")
            is_valid = False

        if User.get_by_email({'email':form_data['email']}):
            flash("Email already exists",'email')
            is_valid = False



        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"

        new_user_id = connectToMySQL('sasquatch').query_db(query,data)

        return new_user_id

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL('sasquatch').query_db(query,data)

        if len(results) < 1:
            return False
        
        return cls(results[0])

    