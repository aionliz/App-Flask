from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Quote:
    db_name = 'favorite_quotes'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.message = data['message']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO quotes (name, message, user_id) VALUES (%(name)s, %(message)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quotes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_quotes = []
        for row in results:
            all_quotes.append(cls(row))
        return all_quotes
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM quotes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update(cls, data):
        query = "UPDATE quotes SET name = %(name)s, message = %(message)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM quotes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_quote(quote):
        is_valid = True
        if len(quote['name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters", "quote")
        if len(quote['message']) < 10:
            is_valid = False
            flash("Message must be at least 10 characters", "quote")
        return is_valid

