'''
Models are helpers to store data
- or methods to retrieve user objects
- internal representation of an entity
'''

from db import db

# Extend db.model

class UserModel(db.Model):
    # SQLAlchemy variables
    __tablename__ = "users"
    # Auto incrementing ids
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # Variable names must match SQLAlchemy ones
        # _id variable removed as SQLAlchemy auto generates
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()