from sqlalchemy.orm import validates
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash

from yumroad.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError('needs to have a name')
        return name
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(), nullable=False)

    @classmethod
    def create(cls, email, password):
        if not email or not password:
            raise ValueError('email and password are required')
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)
