
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, MoviePost  # adjust import if needed

movie_post_bp = Blueprint('movie_post_bp', __name__, url_prefix='/api/posts')

# GET all movie posts
@movie_post_bp.route('/', methods=['GET'])
def get_movie_posts():
    posts = MoviePost.query.all()
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "poster_url": post.poster_url,
            "review": post.review,
            "rating": post.rating,
            "user_id": post.user_id,
            "club_id": post.club_id,
            "timestamp": post.timestamp.isoformat()
        })
    return jsonify(result), 200

# POST a new movie post
@movie_post_bp.route('/', methods=['POST'])
@jwt_required()
def create_movie_post():
    data = request.get_json()
    user_id = get_jwt_identity()

    title = data.get('title')
    review = data.get('review') or data.get('content')  # support both names

    if not title or not review:
        return jsonify({"error": "Title and review/content are required."}), 400

    try:
        new_post = MoviePost(
            title=title,
            poster_url=data.get('poster_url'),
            review=review,
            rating=data.get('rating'),
            user_id=user_id,
            club_id=data.get('club_id')  # optional
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
                "user_id": new_post.user_id,
                "club_id": new_post.club_id,
                "poster_url": new_post.poster_url,
                "timestamp": new_post.timestamp.isoformat(),
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create post", "details": str(e)}), 500

