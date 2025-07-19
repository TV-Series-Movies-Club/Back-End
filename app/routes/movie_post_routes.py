from flask import Blueprint, request, jsonify
from app.models import db, MoviePost, User
from flask_jwt_extended import jwt_required, get_jwt_identity

movie_post_bp = Blueprint('movie_post_bp', __name__)

@movie_post_bp.route('/', methods=['POST'])
@jwt_required()
def create_movie_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_post = MoviePost(
        title=data.get('title'),
        poster_url=data.get('poster_url'),
        review=data.get('review'),
        rating=data.get('rating'),
        user_id=user_id,
        club_id=data.get('club_id')  
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

@movie_post_bp.route('/', methods=['GET'])
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
            "club_id": post.club_id,
            "timestamp": post.timestamp.isoformat()
        }
        for post in posts
    ]), 200

@movie_post_bp.route('/<int:id>', methods=['GET'])
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
        "club_id": post.club_id,
        "timestamp": post.timestamp.isoformat()
    })

@movie_post_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = MoviePost.query.get_or_404(id)
    user_id = get_jwt_identity()

    if post.user_id != user_id:
        return jsonify({"error": "Not authorized"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200

@movie_post_bp.route('/user/<int:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = MoviePost.query.filter_by(user_id=user_id).order_by(MoviePost.timestamp.desc()).all()
    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "poster_url": post.poster_url,
            "review": post.review,
            "rating": post.rating,
            "club_id": post.club_id,
            "timestamp": post.timestamp.isoformat()
        }
        for post in posts
    ]), 200

@movie_post_bp.route('/club/<int:club_id>', methods=['GET'])
def get_posts_by_club(club_id):
    posts = MoviePost.query.filter_by(club_id=club_id).order_by(MoviePost.timestamp.desc()).all()
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
