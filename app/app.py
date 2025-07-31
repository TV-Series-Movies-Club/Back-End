import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import timedelta

from app.models import db
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.movie_post_routes import movie_post_bp
from app.routes.club_routes import club_bp
from app.routes.comment_feed_routes import feed_bp
from app.routes.watch_routes import watch_bp  

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://movie_user:newpassword123@localhost/movies_club'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-super-secret-key'  
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

# Init extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# ----------------------
# ✅ Logging Setup
# ----------------------
logging.basicConfig(level=logging.INFO)  # or logging.DEBUG for more detail
logger = logging.getLogger(__name__)

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled Exception: {e}", exc_info=True)
    return jsonify({"error": "Internal Server Error"}), 500

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(movie_post_bp, url_prefix="/posts")
app.register_blueprint(club_bp, url_prefix="/clubs")
app.register_blueprint(feed_bp, url_prefix="/feed")
app.register_blueprint(watch_bp, url_prefix="/watch")  

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the TV & Movies Club API!"})

@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_access_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify(access_token=new_access_token), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

# ----------------------
# ✅ Run the App
# ----------------------
if __name__ == '__main__':
    app.run(debug=True)
