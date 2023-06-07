"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model for Blogly"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=False, default='https://img.freepik.com/free-icon/user_318-563642.jpg')

    @property
    def full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}"
    
    posts = db.relationship('Post', backref='author')

    posts = db.relationship('Post', backref='author', cascade="all, delete-orphan")

class Post(db.Model):
    """Post Model for Blogly"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # author = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):
    """Tag Model for Blogly"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

class PostTag(db.Model):
    """Model that joins together Post and Tag"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
