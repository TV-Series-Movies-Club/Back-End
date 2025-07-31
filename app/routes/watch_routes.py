from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Watch
from datetime import datetime
import logging

# Setup logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    # fallback in case logging is not set globally
    logging.basicConfig(level=logging.DEBUG)

watch_bp = Blueprint('watch_bp', __name__, url_prefix='/watch')

@watch_bp.route('/', methods=['POST'])
@jwt_required()
def add_watched_movie():
    """
    Log a movie as watched with optional metadata.
    Requires JWT token.
    """
    try:
        data = request.get_json(force=True)
        user_id = get_jwt_identity()

        movie_title = data.get('movie_title')
        year = data.get('year')
        genre = data.get('genre')
        rating = data.get('rating')
        notes = data.get('notes')  # replaces 'experience'
        watched_on_str = data.get('watched_on')

        if not movie_title:
            return jsonify({"error": "Movie title is required"}), 400

        # Validate year
        if year != "" and year is not None:
            try:
                year = int(year)
            except ValueError:
                return jsonify({"error": "Year must be a number"}), 400
        else:
            year = None

        # Validate rating
        if rating != "" and rating is not None:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    return jsonify({"error": "Rating must be between 1 and 5"}), 400
            except ValueError:
                return jsonify({"error": "Rating must be a number"}), 400
        else:
            rating = None

        # Validate date
        try:
            watched_on = datetime.strptime(watched_on_str, "%Y-%m-%d").date() if watched_on_str else datetime.utcnow().date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        watched = Watch(
            movie_title=movie_title,
            year=year,
            genre=genre,
            rating=rating,
            notes=notes,
            watched_on=watched_on,
            user_id=user_id
        )

        db.session.add(watched)
        db.session.commit()

        return jsonify({
            "message": "Movie logged successfully",
            "watch": {
                "id": watched.id,
                "movie_title": watched.movie_title,
                "year": watched.year,
                "genre": watched.genre,
                "rating": watched.rating,
                "notes": watched.notes,
                "watched_on": watched.watched_on.isoformat()
            }
        }), 201

    except Exception as e:
        logger.error(f"[WATCH POST ERROR] {e}", exc_info=True)
        return jsonify({"error": "Internal server error while adding watched movie"}), 500


@watch_bp.route('/', methods=['GET'])
@jwt_required()
def get_watched_movies():
    """
    Retrieve a paginated list of all movies watched by the current user.
    """
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = Watch.query.filter_by(user_id=user_id) \
                                .order_by(Watch.watched_on.desc()) \
                                .paginate(page=page, per_page=per_page, error_out=False)

        watches = pagination.items

        return jsonify({
            "movies": [
                {
                    "id": w.id,
                    "movie_title": w.movie_title,
                    "year": w.year,
                    "genre": w.genre,
                    "rating": w.rating,
                    "notes": w.notes,
                    "watched_on": w.watched_on.isoformat()
                }
                for w in watches
            ],
            "page": page,
            "per_page": per_page,
            "total": pagination.total
        }), 200

    except Exception as e:
        logger.error(f"[WATCH GET ERROR] {e}", exc_info=True)
        return jsonify({"error": "Internal server error while retrieving watched movies"}), 500
