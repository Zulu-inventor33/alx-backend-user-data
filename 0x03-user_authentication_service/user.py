#!/usr/bin/env python3
"""
User model for user authentication system.
This file defines the User class using SQLAlchemy and maps it to the
`users` table in the database.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    """
    User class representing a user record in the 'users' table.

    Attributes:
        id (int): Primary key for the user.
        email (str): Email of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str, optional): Session ID for the user, nullable.
        reset_token (str, optional): Token for password reset, nullable.
    """

    # Mapping the 'users' table to the User model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    hashed_password = db.Column(db.String(250), nullable=False)
    session_id = db.Column(db.String(250), nullable=True)
    reset_token = db.Column(db.String(250), nullable=True)

    def __init__(self, email, hashed_password, session_id=None,
                 reset_token=None):
        """
        Initialize a new user.

        Args:
            email (str): Email address of the user.
            hashed_password (str): Hashed password of the user.
            session_id (str, optional): Session ID for the user.
            reset_token (str, optional): Token for resetting the password.
        """
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token
