from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from models import db
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.movie_post_routes import movie_post_bp  # ✅ Corrected import
from routes.club_routes import club_bp
from routes.comment_feed_routes import feed_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies_club.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # ⚠️ Change in production

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(movie_post_bp)  # ✅ Corrected registration
app.register_blueprint(club_bp)
app.register_blueprint(feed_bp)

# Default route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the TV & Movies Club API!"})

# Handle 404 errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
