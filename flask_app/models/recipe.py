from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.lib.validator import (
    is_length,
    is_email,
    is_password,
    is_match,
    is_present,
)


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.is_under_30_min = data["is_under_30_min"]
        self.cook_date = data["cook_date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate(data):
        messages = []
        if not is_length(data["name"], min=3, max=50):
            messages.append(
                {
                    "message": "Name must be between 3 and 100 characters.",
                    "category": "name",
                }
            )
        if not is_length(data["description"], min=3, max=1000):
            messages.append(
                {
                    "message": "Description must be between 3 and 1000 characters.",
                    "category": "description",
                }
            )
        if not is_length(data["instructions"], min=3, max=1000):
            messages.append(
                {
                    "message": "Instructions must be between 3 and 1000 characters.",
                    "category": "instructions",
                }
            )
        if not is_present(data["cook_date"]):
            messages.append(
                {
                    "message": "Cook date is required",
                    "category": "cook_date",
                }
            )
        return messages

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO recipes (user_id, name, description, instructions, is_under_30_min, cook_date) VALUES (%(user_id)s,%(name)s,%(description)s,%(instructions)s,%(is_under_30_min)s, %(cook_date)s);
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def read(cls, data):
        query = """
            SELECT *, users.first_name FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            recipe_data = {**results[0]}
            recipe_data.pop("first_name")
            recipe_instance = cls(recipe_data)
            recipe_instance.chef = results[0]["users.first_name"]
            return recipe_instance
        return results

    @classmethod
    def read_all(cls):
        query = """
            SELECT *, users.id, users.first_name FROM recipes JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name": row["users.first_name"],
                }
                this_recipe.chef = user_data
                all_recipes.append(this_recipe)
        return all_recipes

    @classmethod
    def read_by_user(cls, data):
        query = """
            SELECT * FROM recipes WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def update(cls, data):
        query = """
            UPDATE recipes 
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cook_date = %(cook_date)s, is_under_30_min = %(is_under_30_min)s
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = """
            DELETE FROM recipes 
            WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
