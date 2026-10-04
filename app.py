from flask import Flask, jsonify, request, render_template
from config import Config
from models import db
from routes.api import api
from routes.pages import pages
def create_app():
    app = Flask(__name__); app.config.from_object(Config)
    db.init_app(app); app.register_blueprint(api); app.register_blueprint(pages)
    with app.app_context(): db.create_all()
    @app.errorhandler(Exception)
    def err(e):
        code = getattr(e, "code", 500)
        if request.path.startswith("/api"): return jsonify(success=False, error="Request failed"), code
        return render_template("error.html", code=code), code
    return app
app = create_app()
if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)
