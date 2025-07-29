from app import db
from datetime import datetime


# Association table for followers (self-referential many-to-many)
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# Association table for users and movie clubs
user_club = db.Table(
    'user_club',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('club_id', db.Integer, db.ForeignKey('movie_clubs.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    # Relationships
    posts = db.relationship('MoviePost', back_populates='user', cascade='all, delete-orphan')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete-orphan')
    joined_clubs = db.relationship('MovieClub', secondary=user_club, back_populates='members')
    watched_movies = db.relationship('Watch', back_populates='user', cascade='all, delete-orphan')
    created_clubs = db.relationship('MovieClub', back_populates='creator', cascade='all, delete-orphan')

    followed = db.relationship(
        'User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )


class MoviePost(db.Model):
    __tablename__ = 'movie_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(500))
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('movie_clubs.id'))

    # Relationships
    user = db.relationship('User', back_populates='posts')
    club = db.relationship('MovieClub', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('movie_posts.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('MoviePost', back_populates='comments')


class MovieClub(db.Model):
    __tablename__ = 'movie_clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50))

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    creator = db.relationship('User', back_populates='created_clubs')
    posts = db.relationship('MoviePost', back_populates='club', cascade='all, delete-orphan')
    members = db.relationship('User', secondary=user_club, back_populates='joined_clubs')


class Watch(db.Model):
    __tablename__ = 'watches'

    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(255), nullable=False)
    watched_on = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    experience = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='watched_movies')
