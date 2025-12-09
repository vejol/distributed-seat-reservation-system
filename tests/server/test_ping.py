"""
Test suite for server health endpoints (ping/pong)
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask
from server.routes.health import health_bp


@pytest.fixture
def app():
    """Create a Flask app for testing"""
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()


class TestPingPong:
    """Test suite for ping/pong health check"""
    
    def test_ping_returns_pong(self, client):
        """Test that /ping endpoint returns 'pong' message"""
        response = client.get('/ping')
        
        assert response.status_code == 200
        assert response.json == {'message': 'pong'}
    
    def test_ping_returns_json(self, client):
        """Test that /ping returns JSON content type"""
        response = client.get('/ping')
        
        assert 'application/json' in response.content_type
