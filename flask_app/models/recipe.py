# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']    
        self.instructions = data['instructions']
        self.under_30_min = data['under_30_min']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM recipes;'
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances of table
        recipes = []
        # Iterate over the db results and create instances of table with cls.
        for recipe_row in results:
            recipes.append( cls(recipe_row) )
        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes WHERE id=%(id)s;'
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls( results[0] )

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under_30_min, date_made, created_at, updated_at, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_30_min)s,%(date_made)s,NOW(),NOW(),%(user_id)s);'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description=%(description)s, instructions=%(instructions)s, under_30_min=%(under_30_min)s, date_made=%(date_made)s, updated_at=NOW() WHERE id = %(id)s;'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL('recipes_schema').query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        #name, description, instructions >= 3 characters:
        if len(data["name"]) < 3 or len(data["description"]) < 3 or len(data["instructions"]) < 3:
            flash("Name, description, and instructions must be longer than 3 characters.", "recipe_error")
            is_valid = False
        
        #date made and under 30 are checked:
        if not data["under_30_min"] or not data["date_made"]:
            flash("All fields must be filled out", "recipe_error")
            is_valid = False
        
        return is_valid