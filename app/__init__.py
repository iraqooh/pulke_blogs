from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    # filename='app.log',
    # filemode='a'
)

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app():
    logging.info('Loading dotenv')
    load_dotenv()
    logging.info('Creating Flask application')
    app = Flask(__name__)
    logging.info('Creating a rate limiter')
    limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour", "20 per minute"])
    logging.info('Loading configuration')
    app.config.from_object('config.Config')

    # Initializing extensions
    logging.info('Initializing extensions')
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Registering route blueprints
    from .routes.health import health_bp
    from .routes.auth import auth_bp
    from .routes.bookmark_routes import bookmarks_bp
    from .routes.views import views_bp
    from app.routes.categories import categories_bp
    from app.routes.tags import tags_bp
    
    logging.info('Registering route blueprints')
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(tags_bp)

    return app