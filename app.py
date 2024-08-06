from flask import Flask
from config import Config
from routes.user_routes import user_bp
from routes.role_routes import role_bp
from routes.ui_routes import ui_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(user_bp, url_prefix='/admin')
app.register_blueprint(role_bp, url_prefix='/admin')
app.register_blueprint(ui_bp, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
