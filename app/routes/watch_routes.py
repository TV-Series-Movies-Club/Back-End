from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Watch, User

watch_bp = Blueprint('watch_bp', __name__, url_prefix='/watch')

@watch_bp.route('/', methods=['POST'])
@jwt_required()
def add_watched_movie():
    """
    Log a movie as watched with an optional user experience description.
    Requires JWT token.
    """
    data = request.get_json()
    user_id = get_jwt_identity()

    movie_title = data.get('movie_title')
    experience = data.get('experience')

    if not movie_title:
        return jsonify({"error": "Movie title is required"}), 400

    watched = Watch(
        movie_title=movie_title,
        experience=experience,
        user_id=user_id
    )
    db.session.add(watched)
    db.session.commit()

    return jsonify({
        "message": "Movie logged successfully",
        "watch": {
            "id": watched.id,
            "movie_title": watched.movie_title,
            "experience": watched.experience,
            "watched_on": watched.watched_on.isoformat()
        }
    }), 201


@watch_bp.route('/', methods=['GET'])
@jwt_required()
def get_watched_movies():
    """
    Retrieve a paginated list of all movies watched by the currently authenticated user.
    Supports pagination with ?page=<page_number>&per_page=<items_per_page>
    """
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Watch.query.filter_by(user_id=user_id)\
                            .order_by(Watch.watched_on.desc())\
                            .paginate(page=page, per_page=per_page, error_out=False)
    
    watches = pagination.items

    return jsonify({
        "movies": [
            {
                "id": w.id,
                "movie_title": w.movie_title,
                "experience": w.experience,
                "watched_on": w.watched_on.isoformat()
            }
            for w in watches
        ],
        "page": page,
        "per_page": per_page,
        "total": pagination.total
    }), 200
