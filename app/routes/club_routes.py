from flask import Blueprint, request, jsonify
from app.models import db, MovieClub, User
from flask_jwt_extended import jwt_required, get_jwt_identity

club_bp = Blueprint('club_bp', __name__, url_prefix='/clubs')


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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    clubs_paginated = MovieClub.query.paginate(page=page, per_page=per_page, error_out=False)

    clubs_data = [
        {
            "id": club.id,
            "name": club.name,
            "description": club.description,
            "genre": club.genre,
            "creator": club.creator.username if club.creator else None
        } for club in clubs_paginated.items
    ]

    return jsonify({
        "clubs": clubs_data,
        "total": clubs_paginated.total,
        "page": clubs_paginated.page,
        "per_page": clubs_paginated.per_page,
        "pages": clubs_paginated.pages
    }), 200


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

   
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    posts_query = club.posts.order_by(db.desc(db.func.coalesce(db.func.length(MovieClub.name), 0))) 
    posts_paginated = posts_query.paginate(page=page, per_page=per_page, error_out=False)

    posts_data = [
        {
            "id": post.id,
            "title": post.title,
            "poster_url": post.poster_url,
            "review": post.review,
            "rating": post.rating,
            "timestamp": post.timestamp.isoformat(),
            "user_id": post.user_id,
            "username": post.user.username if post.user else None
        } for post in posts_paginated.items
    ]

    return jsonify({
        "posts": posts_data,
        "total": posts_paginated.total,
        "page": posts_paginated.page,
        "per_page": posts_paginated.per_page,
        "pages": posts_paginated.pages
    }), 200
