from flask import Blueprint, request, jsonify
from app.models import db, MovieClub, User
from flask_jwt_extended import jwt_required, get_jwt_identity

club_bp = Blueprint('club_bp', __name__)

@club_bp.route('/', methods=['POST']) 
@jwt_required()
def create_club():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    new_club = MovieClub(
        name=data.get('name'),
        description=data.get('description'),
        genre=data.get('genre'),
        creator_id=current_user_id
    )
    db.session.add(new_club)
    db.session.commit()

    return jsonify({
        "message": "Club created successfully",
        "club": {
            "id": new_club.id,
            "name": new_club.name,
            "description": new_club.description,
            "genre": new_club.genre,
            "creator_id": new_club.creator_id
        }
    }), 201

@club_bp.route('/', methods=['GET'])  
def get_clubs():
    clubs = MovieClub.query.all()
    return jsonify([
        {
            "id": club.id,
            "name": club.name,
            "description": club.description,
            "genre": club.genre,
            "creator": club.creator.username if club.creator else None
        } for club in clubs
    ]), 200

@club_bp.route('/join/<int:club_id>', methods=['POST'])  
@jwt_required()
def join_club(club_id):
    user_id = get_jwt_identity()
    club = MovieClub.query.get_or_404(club_id)
    user = User.query.get(user_id)

    if user in club.members:
        return jsonify({"message": "Already a member"}), 400

    club.members.append(user)
    db.session.commit()

    return jsonify({"message": f"Joined club {club.name}"}), 200

@club_bp.route('/<int:club_id>/leave', methods=['POST'])  
@jwt_required()
def leave_club(club_id):
    user = User.query.get(get_jwt_identity())
    club = MovieClub.query.get_or_404(club_id)

    if club not in user.joined_clubs:
        return jsonify({"message": "Not a member"}), 400

    user.joined_clubs.remove(club)
    db.session.commit()
    return jsonify({"message": f"Left club '{club.name}'"}), 200

@club_bp.route('/<int:club_id>/posts', methods=['GET']) 
def get_club_posts(club_id):
    club = MovieClub.query.get_or_404(club_id)
    posts = club.posts  

    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "poster_url": post.poster_url,
            "review": post.review,
            "rating": post.rating,
            "timestamp": post.timestamp.isoformat(),
            "user_id": post.user_id,
            "username": post.user.username if post.user else None
        } for post in posts
    ]), 200
