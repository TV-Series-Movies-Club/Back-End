import os
import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # App Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///movies_club.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # -------------------
    # Setup Logging
    # -------------------
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # You can also use file logging like this:
    # logging.basicConfig(filename='error.log', level=logging.ERROR)

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error("Unhandled Exception: %s", e, exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

    # Register Blueprints
    try:
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
    except ImportError as e:
        app.logger.error("[Blueprint Error] Failed to register blueprints", exc_info=True)

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to the Movies Club API!"})

    return app
