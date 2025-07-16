from app.extensions import db
from flask_login import UserMixin


class QAPair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(512), unique=True, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Store plain text password

    def set_password(self, password):
        # Directly assign the password without hashing
        self.password = password

    def check_password(self, password):
        # Directly compare the provided password with the stored password
        return self.password == password
