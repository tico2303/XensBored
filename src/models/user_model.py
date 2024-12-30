from . import db
from sqlalchemy import func
from sqlalchemy.orm import object_session
from sqlalchemy.orm.attributes import flag_modified


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=True)  # Unique email
    zipcode = db.Column(db.String(10), nullable=True)  # Optional Zipcode
    isLoggedIn = db.Column(db.Boolean, default=False)  # Login status
    energyLevel = db.Column(db.Integer, default=5)  # Engery level
    interests = db.Column(
        db.JSON,
        nullable=True,
        default={
            "indoor": [],
            "outdoor": [],
            "indoor and outdoor": [],
            "social": [],
        },
    )  # interests (stored as JSON)
    chat_history = db.Column(db.JSON, nullable=True)  # Chat history (stored as JSON)

    def __repr__(self):
        return f"<User {self.username}>"

    def __setattr__(self, key, value):
        """
        Automatically commit changes after setting an attribute.
        """
        # Use the default setattr to update the attribute
        super().__setattr__(key, value)

        # exclude the intestests from the commit
        if key in ["interests"]:
            return
        # Get the session and commit the changes if the object is already in a session
        session = object_session(self)
        if session:
            session.commit()

    @classmethod
    def query_user(cls, username):
        if not username:
            return None
        return cls.query.filter(func.lower(cls.username) == username.lower()).first()

    @classmethod
    def clear_preferences(cls, username):
        user = cls.query.filter(func.lower(cls.username) == username.lower()).first()
        if user:
            user.energyLevel = 5
            user.zipcode = None
            user.interests = None
            db.session.commit()
            print(f"Cleared preferences for user {username}.")
        else:
            print(f"User {username} not found.")

    @classmethod
    def update_preferences(
        cls, username, category, items, energyLevel=None, zipCode=None
    ):
        user = cls.query.filter(func.lower(cls.username) == username.lower()).first()
        if user:
            User.update_interests(username, category, items)
            user.energyLevel = energyLevel
            user.zipcode = zipCode
            db.session.commit()
            db.session.refresh(user)
            print(f"Updated preferences for user {username}: {user.interests}")
            print("returning user: ", user)
            user = User.query_user(username)
            return user
        else:
            print(f"User {username} not found.")
        return None

    @classmethod
    def update_interests(cls, username, category, items):
        user = cls.query.filter(func.lower(cls.username) == username.lower()).first()
        if user:
            if user.interests is None:
                user.interests = {}

            if category not in user.interests:
                user.interests[category] = []

            for item in items:
                if item not in user.interests[category]:
                    user.interests[category].append(item)

            flag_modified(user, "interests")

            db.session.commit()
            print(f"Updated interests for user {username}: {user.interests}")
        else:
            print(f"User {username} not found.")

    def to_json(self, exclude=[]):
        """Convert the User object to a JSON-serializable dictionary."""
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "zipcode": self.zipcode,
            "energyLevel": self.energyLevel,
            "isLoggedIn": self.isLoggedIn,
            "interests": self.interests,
            "chat_history": self.chat_history,
        }
        for key in exclude:
            data.pop(key, None)
        return data
