from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=True)  # Unique email
    zipcode = db.Column(db.String(10), nullable=True)  # Optional Zipcode
    isLoggedIn = db.Column(db.Boolean, default=False)  # Login status
    interests = db.Column(db.JSON, nullable=True)  # List of interests (stored as JSON)
    chat_history = db.Column(db.JSON, nullable=True)  # Chat history (stored as JSON)

    def __repr__(self):
        return f"<User {self.username}>"

    def to_json(self, exclude=[]):
        """Convert the User object to a JSON-serializable dictionary."""
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "zipcode": self.zipcode,
            "isLoggedIn": self.isLoggedIn,
            "interests": self.interests,
            "chat_history": self.chat_history,
        }
        for key in exclude:
            data.pop(key, None)
        return data
