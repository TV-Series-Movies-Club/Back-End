from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Association table: User following
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

# Association table: Club membership
club_members = db.Table('club_members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('movie_clubs.id'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Relationships
    posts = db.relationship('MoviePost', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    created_clubs = db.relationship('MovieClub', backref='creator', lazy=True)
    joined_clubs = db.relationship('MovieClub', secondary=club_members, back_populates='members')

    # Follow system
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


class MovieClub(db.Model):
    __tablename__ = 'movie_clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    genre = db.Column(db.String)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    members = db.relationship('User', secondary=club_members, back_populates='joined_clubs')
    posts = db.relationship('MoviePost', backref='club', lazy=True)


class MoviePost(db.Model):
    __tablename__ = 'movie_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    poster_url = db.Column(db.String)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('movie_clubs.id'))

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete')


# app/models.py

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('movie_posts.id'), nullable=False)

    user = db.relationship('User', backref='comments')
    post = db.relationship('MoviePost', backref='comments')  # <- THIS is missing

