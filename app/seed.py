#!/usr/bin/env python3

from app import app, db
from models import User, MovieClub, MoviePost, Comment
from werkzeug.security import generate_password_hash

with app.app_context():
    print("🔄 Dropping all tables...")
    db.drop_all()
    print("🛠️ Creating all tables...")
    db.create_all()

    # Create Users
    print("👤 Creating users...")
    user1 = User(username='alice', email='alice@example.com', password_hash=generate_password_hash('password'))
    user2 = User(username='bob', email='bob@example.com', password_hash=generate_password_hash('password'))
    user3 = User(username='charlie', email='charlie@example.com', password_hash=generate_password_hash('password'))

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Following
    print("🔁 Adding follows...")
    user1.follow(user2)
    user2.follow(user3)
    db.session.commit()

    # Movie Clubs
    print("🎬 Creating movie clubs...")
    club1 = MovieClub(name="Action Fans", description="All about action movies", genre="Action", creator=user1)
    club2 = MovieClub(name="Drama Club", description="Discuss dramatic masterpieces", genre="Drama", creator=user2)

    club1.members.extend([user1, user2])
    club2.members.extend([user2, user3])

    db.session.add_all([club1, club2])
    db.session.commit()

    # Movie Posts
    print("📝 Creating movie posts...")
    post1 = MoviePost(title="Inception", poster_url="", review="Mind-blowing!", rating=5, user=user1)
    post2 = MoviePost(title="The Godfather", poster_url="", review="Classic crime drama", rating=5, user=user2)
    post3 = MoviePost(title="Titanic", poster_url="", review="Heartbreaking but beautiful", rating=4, user=user3)

    db.session.add_all([post1, post2, post3])
    db.session.commit()

    # Comments
    print("💬 Adding comments...")
    comment1 = Comment(content="Absolutely loved it!", user=user2, post=post1)
    comment2 = Comment(content="Timeless masterpiece!", user=user3, post=post2)
    comment3 = Comment(content="Too emotional 😭", user=user1, post=post3)

    db.session.add_all([comment1, comment2, comment3])
    db.session.commit()

    print("✅ Seeding complete!")
