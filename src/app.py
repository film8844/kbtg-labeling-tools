from flask import Flask
from flask_login import LoginManager, login_required,current_user,UserMixin,login_user,logout_user
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from flask_dropzone import Dropzone



db = SQLAlchemy()
login_manager = LoginManager()
dropzone = Dropzone()

UPLOAD_FOLDER = 'static/images/'

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'kbtg'
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    basedir = os.path.abspath(
        os.path.dirname(__file__)
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    #                                         'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    dropzone.init_app(app)
    
    from routes.auth import router as auth_router
    from routes.main import router as main_router
    from routes.api import router as api_router
    
    app.register_blueprint(auth_router)
    app.register_blueprint(main_router)
    app.register_blueprint(api_router)
    
    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        """ load_user """
        return User.query.get(int(user_id))

    return app