from flask import Flask
from .config import DEBUG
from .routes.api import api_bp
from .routes.views import views_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    app.register_blueprint(views_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=DEBUG)
