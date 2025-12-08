from flask import Flask
from flask_cors import CORS
from .routes import register_routes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register all routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

