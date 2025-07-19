from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

follow_bp = Blueprint('follow_bp', __name__)

# Follow a user
@follow_bp.route('/follow/<int:user_id>', methods=['POST'])
@jwt_required()
def follow_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)

    if not target_user:
        return jsonify({"error": "User not found"}), 404
    if current_user.id == target_user.id:
        return jsonify({"error": "You cannot follow yourself"}), 400

    current_user.follow(target_user)
    db.session.commit()
    return jsonify({"message": f"You are now following {target_user.username}"}), 200

# Unfollow a user
@follow_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@jwt_required()
def unfollow_user(user_id):
    current_user = User.query.get(get_jwt_identity())
    target_user = User.query.get(user_id)

    if not target_user:
        return jsonify({"error": "User not found"}), 404
    if current_user.id == target_user.id:
        return jsonify({"error": "You cannot unfollow yourself"}), 400

    current_user.unfollow(target_user)
    db.session.commit()
    return jsonify({"message": f"You have unfollowed {target_user.username}"}), 200

# Get followers of a user
@follow_bp.route('/users/<int:user_id>/followers', methods=['GET'])
def get_followers(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    followers = [{"id": u.id, "username": u.username} for u in user.followers]
    return jsonify({"followers": followers}), 200

# Get users followed by a user
@follow_bp.route('/users/<int:user_id>/following', methods=['GET'])
def get_following(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    following = [{"id": u.id, "username": u.username} for u in user.followed]
    return jsonify({"following": following}), 200
user_bp = follow_bp
