from flask import Blueprint, request, jsonify
from app.models import db, MoviePost, User
from flask_jwt_extended import jwt_required, get_jwt_identity

movie_post_bp = Blueprint('movie_post_bp', __name__, url_prefix='/posts')


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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_posts = MoviePost.query.order_by(MoviePost.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "posts": [
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
            } for post in paginated_posts.items
        ],
        "total": paginated_posts.total,
        "page": paginated_posts.page,
        "per_page": paginated_posts.per_page,
        "pages": paginated_posts.pages
    }), 200


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
  
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    user = User.query.get_or_404(user_id)
    paginated_posts = MoviePost.query.filter_by(user_id=user_id)\
        .order_by(MoviePost.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "poster_url": post.poster_url,
                "review": post.review,
                "rating": post.rating,
                "club_id": post.club_id,
                "timestamp": post.timestamp.isoformat()
            } for post in paginated_posts.items
        ],
        "total": paginated_posts.total,
        "page": paginated_posts.page,
        "per_page": paginated_posts.per_page,
        "pages": paginated_posts.pages
    }), 200


@movie_post_bp.route('/club/<int:club_id>', methods=['GET'])
def get_posts_by_club(club_id):
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_posts = MoviePost.query.filter_by(club_id=club_id)\
        .order_by(MoviePost.timestamp.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "posts": [
            {
                "id": post.id,
                "title": post.title,
                "poster_url": post.poster_url,
                "review": post.review,
                "rating": post.rating,
                "user_id": post.user_id,
                "username": post.user.username,
                "timestamp": post.timestamp.isoformat()
            } for post in paginated_posts.items
        ],
        "total": paginated_posts.total,
        "page": paginated_posts.page,
        "per_page": paginated_posts.per_page,
        "pages": paginated_posts.pages
    }), 200
