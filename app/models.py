"""Models for Blogly."""
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
import datetime 

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
 
class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False , default=datetime.datetime.utcnow)
    # , default=datetime.datetime.utcnow
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
    post_tags = db.relationship('PostTag', backref='post', cascade='all, delete-orphan')

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(
        db.String(),
        nullable=False,
        default="https://www.freeiconspng.com/thumbs/person-icon/gray-person-icon-27.png",
    )

    @property
    def full_name(self):
        """Return full name of user."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    post_tags = db.relationship('PostTag', backref='tag', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        return f'<PostTag post_id={self.post_id}, tag_id={self.tag_id}>'

       