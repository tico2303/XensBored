from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True)  # Unique username
    email = db.Column(db.String(120), unique=True)  # Unique email

    def __repr__(self):
        return f"<User {self.username}>"
