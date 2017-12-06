# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """
    Create a User table
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    img_url = db.Column(db.String(128))
    foods = db.relationship('Food', backref='user', lazy='dynamic')
    # users = db.relationship('Upvote_user', backref='upvote_user', lazy='dynamic')
    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hased password
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)


# Set up User_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Food(db.Model):
    """
    Create a Food table
    """

    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    img_url = db.Column(db.String(128))
    desc = db.Column(db.String(1500))
    test = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    step = db.relationship('Step', backref='food', lazy='dynamic')

    def __repr__(self):
        return '<Food: {}>'.format(self.name)

class Step(db.Model):
    """
    Create a step table
    """

    __tablename__ = 'step'

    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String(128))
    desc = db.Column(db.String(200))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))

class Upvote(db.Model):
    """
    Create upvote table for like, unlike
    """

    __tablename__ = 'upvote'

    # id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
