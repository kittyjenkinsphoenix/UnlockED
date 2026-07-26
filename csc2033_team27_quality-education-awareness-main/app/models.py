from datetime import datetime

from cryptography.fernet import Fernet
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # store the hash, not the password
    role = db.Column(db.String(50), default="user", nullable=False)
    encrypted_bio = db.Column(db.LargeBinary, nullable=True)  # store encrypted, not a string
    quiz_score = db.Column(db.Integer, default=None, nullable=True)
    high_score = db.Column(db.Integer, default=None, nullable=True)
    first_score = db.Column(db.Integer, default=None, nullable=True)
    quiz_count = db.Column(db.Integer, default=0, nullable=True)
    quiz_results = db.relationship("QuizResult", backref="user", lazy=True)

    def set_password(self, password):
        pepper = current_app.config["SECURITY_PEPPER"]  # add pepper to each password
        if not pepper:
            raise ValueError("Pepper is missing")

        salted_peppered = password + pepper  # combine password w/ pepper
        self.password_hash = generate_password_hash(salted_peppered)  # hash it

    def check_password(self, password):
        pepper = current_app.config["SECURITY_PEPPER"]
        return check_password_hash(
            self.password_hash, password + pepper
        )  # compare user password to stored password (+ pepper)

    def set_bio(self, bio_text):
        if not bio_text:  # if no bio, do nothing (bio is not required)
            return
        key = current_app.config["BIO_ENCRYPTION_KEY"]
        f = Fernet(key.encode())  # turn key into bytes (needed)
        self.encrypted_bio = f.encrypt(bio_text.encode())  # store encrypted bio

    def get_bio(self):
        if not self.encrypted_bio:
            return ""  # no bio, return nothing
        key = current_app.config["BIO_ENCRYPTION_KEY"]
        f = Fernet(key.encode())
        try:
            return f.decrypt(self.encrypted_bio).decode()  # read encrypted bio, return normal text
        except Exception:
            return "Error decrypting"

    def __repr__(self):
        return f"<User {self.username}>"  # clean logging (doesnt return "user")


class MailList(db.Model):
    email = db.Column(db.String(80), unique=True, primary_key=True, nullable=False)


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False, default=6)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
