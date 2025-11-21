from flask import Blueprint

# Import blueprints
from .movies import movies_bp
from .theaters import theaters_bp
from .showtimes import showtimes_bp
from .health import health_bp

def register_routes(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(health_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(theaters_bp)
    app.register_blueprint(showtimes_bp)
