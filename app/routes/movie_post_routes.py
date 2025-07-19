from flask import Blueprint, request, jsonify
from models import db, MoviePost, User
from flask_jwt_extended import jwt_required, get_jwt_identity

movie_post_bp = Blueprint('movie_post_bp', __name__)

# Create a movie post
@movie_post_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_movie_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_post = MoviePost(
        title=data.get('title'),
        poster_url=data.get('poster_url'),
        review=data.get('review'),
        rating=data.get('rating'),
        user_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "message": "Movie post created successfully",
        "post": {
            "id": new_post.id,
            "title": new_post.title,
            "review": new_post.review,
            "rating": new_post.rating,
            "user_id": new_post.user_id
        }
    }), 201

# Get all movie posts
@movie_post_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = MoviePost.query.order_by(MoviePost.timestamp.desc()).all()
    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "poster_url": post.poster_url,
            "review": post.review,
            "rating": post.rating,
            "user_id": post.user_id,
            "username": post.user.username,
            "timestamp": post.timestamp.isoformat()
        }
        for post in posts
    ]), 200

# Get single movie post
@movie_post_bp.route('/posts/<int:id>', methods=['GET'])
def get_single_post(id):
    post = MoviePost.query.get_or_404(id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "poster_url": post.poster_url,
        "review": post.review,
        "rating": post.rating,
        "user_id": post.user_id,
        "username": post.user.username,
        "timestamp": post.timestamp.isoformat()
    })

# Delete post
@movie_post_bp.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = MoviePost.query.get_or_404(id)
    user_id = get_jwt_identity()

    if post.user_id != user_id:
        return jsonify({"error": "Not authorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200
