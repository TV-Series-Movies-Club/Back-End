from app import db  
from datetime import datetime

# Association tables
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

user_club = db.Table(
    'user_club',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('movie_clubs.id'), primary_key=True)
)

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    posts = db.relationship('MoviePost', back_populates='user', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')
    joined_clubs = db.relationship('MovieClub', secondary=user_club, back_populates='members')
    watched_movies = db.relationship('Watch', back_populates='user', cascade='all, delete')

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

# Movie post model
class MoviePost(db.Model):
    __tablename__ = 'movie_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    poster_url = db.Column(db.String)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('movie_clubs.id'))

    user = db.relationship('User', back_populates='posts')
    club = db.relationship('MovieClub', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete')

# Comment model
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('movie_posts.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    post = db.relationship('MoviePost', back_populates='comments')

# ✅ Updated MovieClub model
class MovieClub(db.Model):
    __tablename__ = 'movie_clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    creator = db.relationship('User', backref='created_clubs')  # ✅ Fix: now has a backref
    posts = db.relationship('MoviePost', back_populates='club', cascade='all, delete')
    members = db.relationship('User', secondary=user_club, back_populates='joined_clubs')

# Watch model
class Watch(db.Model):
    __tablename__ = 'watches'

    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(255), nullable=False)
    watched_on = db.Column(db.Date, nullable=False, default=db.func.current_date())
    experience = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='watched_movies')
