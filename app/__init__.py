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
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from app.models import SiconfiDataRREO, SiconfiDataRGF, BrentANP, Focus, IPCA_IBGE, Desemprego_IBGE, CAGED_IBGE,RGF_SICONFI,RREO_SICONFI
        db.create_all()

        from app.routes import main
        app.register_blueprint(main)

        from app.scheduler import start_scheduler
        start_scheduler(app)
    
    return app

