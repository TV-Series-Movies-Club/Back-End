import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///movies_club.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.movie_post_routes import movie_post_bp
    from .routes.club_routes import club_bp
    from .routes.comment_feed_routes import feed_bp
    from .routes.watch_routes import watch_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(movie_post_bp)
    app.register_blueprint(club_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(watch_bp)  

    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Movies Club API!"})

    return app
