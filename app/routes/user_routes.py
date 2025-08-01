from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from app.models import db, User, MoviePost
from datetime import datetime

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def user_to_dict(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_picture": user.profile_picture,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_to_dict(user)), 200

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    username = request.form.get('username')
    email = request.form.get('email')
    file = request.files.get('profile_picture')

    if username:
        user.username = username
    if email:
        user.email = email
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        user.profile_picture = f'/static/uploads/{filename}'

    db.session.commit()
    return jsonify({"message": "Profile updated", "user": user_to_dict(user)}), 200

@user_bp.route('/profile/password', methods=['PUT'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({"error": "Both current and new passwords are required"}), 400

    if not check_password_hash(user.password_hash, current_password):
        return jsonify({"error": "Current password is incorrect"}), 401

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

@user_bp.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)

    if not target_user:
        return jsonify({"error": "User not found"}), 404
    if current_user.id == target_user.id:
        return jsonify({"error": "You cannot follow yourself"}), 400
    if target_user in current_user.followed:
        return jsonify({"message": f"Already following {target_user.username}"}), 400

    current_user.followed.append(target_user)
    db.session.commit()
    return jsonify({"message": f"You are now following {target_user.username}"}), 200

@user_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)

    if not target_user:
        return jsonify({"error": "User not found"}), 404
    if current_user.id == target_user.id:
        return jsonify({"error": "You cannot unfollow yourself"}), 400
    if target_user not in current_user.followed:
        return jsonify({"message": f"You are not following {target_user.username}"}), 400

    current_user.followed.remove(target_user)
    db.session.commit()
    return jsonify({"message": f"You have unfollowed {target_user.username}"}), 200

@user_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start = (page - 1) * per_page
    end = start + per_page

    followers = user.followers[start:end]
    return jsonify({
        "followers": [{"id": u.id, "username": u.username} for u in followers],
        "page": page,
        "per_page": per_page,
        "total": user.followers.count()
    }), 200

@user_bp.route('/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    start = (page - 1) * per_page
    end = start + per_page

    following = user.followed[start:end]
    return jsonify({
        "following": [{"id": u.id, "username": u.username} for u in following],
        "page": page,
        "per_page": per_page,
        "total": user.followed.count()
    }), 200

@user_bp.route('/profile/posts', methods=['GET'])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()
    posts = MoviePost.query.filter_by(user_id=user_id).order_by(MoviePost.id.desc()).all()

    return jsonify([
        {
            "id": post.id,
            "content": post.content,
            "created_at": post.created_at.isoformat() if post.created_at else None
        }
        for post in posts
    ]), 200
