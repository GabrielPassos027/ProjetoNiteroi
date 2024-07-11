# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# from app.models import db
# from app.scheduler import start_scheduler

# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__, template_folder='templates', static_folder='static')
#     app.config.from_object(Config)
#     db.init_app(app)

#     from app.routes import main
#     app.register_blueprint(main)

#     from .models import SiconfiDataRREO
#     from .models import SiconfiDataRREO
#     with app.app_context():
#         db.create_all()
#         start_scheduler()
    

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import Config
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    app.secret_key = 'abcdefgh12345678'

    with app.app_context():
        from app.models import BrentANP, Focus, IPCA_IBGE, Desemprego_IBGE, CAGED_IBGE,RGF_SICONFI,RREO_SICONFI, User
        db.create_all()

        if not User.query.filter_by(username='Niteroi').first():
            user = User(username='Niteroi', password=generate_password_hash('teste', method='pbkdf2:sha256'))
            db.session.add(user)
            db.session.commit()

        from app.routes import main
        app.register_blueprint(main)

        from app.auth import auth
        app.register_blueprint(auth)

        from app.scheduler import start_scheduler
        start_scheduler(app)
    
    return app

