from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Comment, MoviePost, User

feed_bp = Blueprint('feed_bp', __name__)


@feed_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({"error": "Comment content is required"}), 400

    post = MoviePost.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comment = Comment(
        content=content,
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        "message": "Comment added successfully",
        "comment": {
            "id": comment.id,
            "content": comment.content,
            "user_id": comment.user_id,
            "post_id": comment.post_id,
            "timestamp": comment.created_at.isoformat()
        }
    }), 201


@feed_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    post = MoviePost.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()

    return jsonify([
        {
            "id": comment.id,
            "content": comment.content,
            "user": comment.user.username,
            "user_id": comment.user.id,
            "timestamp": comment.created_at.isoformat()
        }
        for comment in comments
    ]), 200
