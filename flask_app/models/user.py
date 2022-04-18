# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[a-zA-Z]+$')
NAME_REGEX = re.compile('[@_!#$%^&*()<>?/}{~:1234567890]')

# model the class after the table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances of table
        users = []
        # Iterate over the db results and create instances of table with cls.
        for user_row in results:
            users.append( cls(user_row) )
        return users

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users LEFT JOIN recipes ON user_id = users.id WHERE users.id = %(id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        
        user = cls( results[0] )

        if results[0]["recipes.id"] != None:
            for row in results:
                recipe_data = {
                    "id": row["recipes.id"],
                    "name": row["name"],
                    "description": row["description"],
                    "instructions": row["instructions"],
                    "under_30_min": row["under_30_min"],
                    "date_made": row["date_made"],
                    "created_at": row["recipes.created_at"],
                    "updated_at": row["recipes.updated_at"],
                    "user_id": row["user_id"]
                }

                user.recipes.append( recipe.Recipe(recipe_data) )

        return user

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users LEFT JOIN recipes ON user_id = users.id WHERE email = %(email)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        if len(results) < 1:
            return False
        
        user = cls( results[0] )

        if results[0]["recipes.id"] != None:
            for row in results:
                recipe_data = {
                    "id": row["recipes.id"],
                    "name": row["name"],
                    "description": row["description"],
                    "instructions": row["instructions"],
                    "under_30_min": row["under_30_min"],
                    "date_made": row["date_made"],
                    "created_at": row["recipes.created_at"],
                    "updated_at": row["recipes.updated_at"],
                    "user_id": row["user_id"]
                }

                user.recipes.append( recipe.Recipe(recipe_data) )

        return user

    @classmethod
    def get_all_emails(cls):
        query = 'SELECT email FROM users;'
        results = connectToMySQL('recipes_schema').query_db(query)
        emails = []
        for email_row in results:
            emails.append(email_row['email'])
        return emails

    @staticmethod
    def validate_registration(user):
        is_valid = True

        #first and last name min of 2 characters
        if len(user['first_name']) < 2 or len(user['last_name']) < 2:
            flash("First and last name must be greater than 2 characters.", "register_error")
            is_valid = False

        #valid chars for first and last name
        if NAME_REGEX.search(user['first_name']) or NAME_REGEX.search(user['last_name']):
            flash("Invalid characters for first and last name", "register_error")
            is_valid = False

        #valid email
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "register_error")
            is_valid = False

        emails = User.get_all_emails()
        if user['email'] in emails:
            flash('Email already registered.', "register_error")
            is_valid = False

        #invalid password
        if (user['password'] != user['password_check']):
            flash("Passwords do not match.", "register_error")
            is_valid = False
        
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register_error")
            is_valid = False

        return is_valid