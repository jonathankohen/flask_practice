# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL


class Friend:
    def __init__(self, data):
        self.id = data["id"]
        self.nickname = data["nickname"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friends;"
        results = connectToMySQL("users_practice").query_db(query)
        friends = []
        for friend in results:
            friends.append(cls(friend))
        return friends

    @classmethod
    def save(cls, data):
        query = "Insert INTO friends (nickname, user_id, created_at, updated_at) VALUES(%(nickname)s, %(user_id)s, NOW(), NOW());"
        friend_id = connectToMySQL("users_practice").query_db(query, data)
        return friend_id

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM friends WHERE id = %(id)s;"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results[0]

    @classmethod
    def update(cls, data):
        query = "UPDATE friends SET nickname = %(nickname)s WHERE id = %(id)s"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM friends WHERE id = %(id)s"
        results = connectToMySQL("users_practice").query_db(query, data)
        return results