from flask_login import AnonymousUserMixin, UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash

from yumroad.extensions import db

Column = db.Column
Model = db.Model
Integer = db.Integer
String = db.String
Text = db.Text
ForeignKey = db.ForeignKey
relationship = db.relationship


class User(UserMixin, db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    password = Column(String(), nullable=False)

    store = relationship("Store", uselist=False, back_populates="user")
    products = relationship("Product", back_populates="creator")

    @classmethod
    def create(cls, email, password):
        if not email or not password:
            raise ValueError("email and password are required")
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)

    @property
    def is_authenticated(self):
        return not isinstance(self, AnonymousUserMixin)


class Product(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(120), nullable=False)
    store_id = Column(Integer, ForeignKey("store.id"))
    creator_id = Column(Integer, ForeignKey("user.id"))
    price_cents = Column(Integer)
    picture_url = Column(Text)

    store = relationship("Store", uselist=False, back_populates="products")
    creator = relationship("User", uselist=False, back_populates="products")

    @validates("name")
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("needs to have a name")
        return name

    @property
    def primary_image_url(self):
        return (
            self.picture_url
            or "https://placehold.co/600x400?text={}".format(self.name)
        )


class Store(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", uselist=False, back_populates="store")
    products = relationship("Product", back_populates="store", lazy="joined")

    @validates("name")
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError("needs to have a name")
        return name
