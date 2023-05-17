from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.lib.validator import (
    is_length,
    is_email,
    is_password,
    is_match,
    is_present,
)


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate(data):
        messages = []
        if not is_length(data["first_name"], min=2, max=100):
            messages.append(
                {
                    "message": "First name must be between 2 and 100 characters.",
                    "category": "first_name",
                }
            )
        if not is_length(data["last_name"], min=2, max=100):
            messages.append(
                {
                    "message": "Last name must be between 2 and 100 characters.",
                    "category": "last_name",
                }
            )
        if not is_present(data["email"]):
            messages.append({"message": "Email is required.", "category": "email"})
        elif not is_email(data["email"]):
            messages.append(
                {"message": "Email must be a valid email address.", "category": "email"}
            )
        if not is_password(data["password"]):
            messages.append(
                {
                    "message": "Password must be between 8 and 72 characters and at least one uppercase letter, one lowercase letter, one number and one special character",
                    "category": "password",
                }
            )
        elif not is_match(data["password"], data["confirm_password"]):
            messages.append(
                {"message": "Passwords do not match.", "category": "confirm_password"}
            )
        return messages

    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        return results

    @classmethod
    def read(cls, data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            user_instance = cls(results[0])
            return user_instance
        return results

    @classmethod
    def read_by_email(cls, data):
        query = """
            SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            user_instance = cls(results[0])
            return user_instance
        return results

    @classmethod
    def read_with_recipes(cls, data):
        query = """
            SELECT  users.first_name, users.last_name, users.email, recipes.name, recipes.is_under_30_min
            FROM users LEFT JOIN recipes on users.id = recipes.user_id
            WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            user_instance = cls(results[0])
            recipe_list = []
            for row in results:
                if row["recipes.id"] == None:
                    return user_instance

                recipe_data = {
                    "id": row["recipes.id"],
                    "name": row["recipes.name"],
                    "is_under_30_min": row["recipes.is_under_30_min"],
                }
                recipe_list.append(recipe_data)

            user_instance.recipes = recipe_list

        return user_instance
