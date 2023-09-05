from flask import Flask
from flask_login import LoginManager, login_required,current_user,UserMixin,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os


db = SQLAlchemy()
login_manager = LoginManager()
UPLOAD_FOLDER = 'static/uploads'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kbtg'

    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    basedir = os.path.abspath(
        os.path.dirname(__file__)
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
                                            'sqlite:///' + os.path.join(basedir, 'database.db')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from routes.auth import router as auth_router
    from routes.main import router as main_router
    
    app.register_blueprint(auth_router)
    app.register_blueprint(main_router)
    
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        """ load_user """
        return User.query.get(int(user_id))

    return app