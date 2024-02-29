from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


class Favorite:
    db_name = 'favorite_quotes'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.quote_id = data['quote_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO favorites (user_id, quote_id) VALUES (%(user_id)s, %(quote_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM favorites;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_favorites = []
        for row in results:
            all_favorites.append(cls(row))
        return all_favorites
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM favorites WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE favorites SET user_id = %(user_id)s, quote_id = %(quote_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM favorites WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_favorite(favorite):
        is_valid = True
        if not favorite['quote_id']:
            is_valid = False
            flash("Please select a quote", "favorite")
        return is_valid