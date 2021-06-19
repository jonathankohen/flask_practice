from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import friend
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.friends = []

    @staticmethod
    def validate_reg(user):
        is_valid = True

        if len(user["first_name"]) == 0:
            flash("Please enter your first name.")
            is_valid = False
        elif len(user["first_name"]) < 2:
            flash("First name must be at least 3 characters.")
            is_valid = False
        elif not str.isalpha(user["first_name"]):
            flash("First name must contain only letters.")
            is_valid = False

        if len(user["last_name"]) == 0:
            flash("Please enter your last name.")
            is_valid = False
        elif len(user["last_name"]) < 2 and str.isalpha(user["last_name"]):
            flash("Last name must be at least 3 characters.")
            is_valid = False
        elif not str.isalpha(user["last_name"]):
            flash("Last name must contain only letters.")
            is_valid = False

        if len(user["email"]) == 0:
            flash("Please enter your email address.")
            is_valid = False
        elif not EMAIL_REGEX.match(user["email"]):
            flash("Invalid email address!")
            is_valid = False

        if len(user["password"]) == 0:
            flash("Please enter your password.")
            is_valid = False
        elif len(user["password"]) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        elif user["password"] != user["c_pw"]:
            flash("Passwords must match.")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("users_practice").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("users_practice").query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL("users_practice").query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results[0]

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results

    @classmethod
    def get_user_with_friends(cls, data):
        query = "SELECT * FROM users LEFT JOIN friends ON friends.users_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL("users_practice").query_db(query, data)
        user = cls(results[0])
        # print(results)
        for row_from_db in results:
            friend_data = {
                "id": row_from_db["friends.id"],
                "nickname": row_from_db["nickname"],
                "created_at": row_from_db["friends.created_at"],
                "updated_at": row_from_db["friends.updated_at"],
            }
            user.friends.append(friend.Friend(friend_data))
        return user