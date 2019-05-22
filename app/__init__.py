import os
import rq
from redis import Redis
from config import Config
from flask import Flask, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('webgame-tasks', connection=app.redis)
    app.task_queue.empty()
    app.task_queue.enqueue('app.tasks.gift_users.gift_users', job_timeout=-1)

    from app.routes import base, shop, auth, google_auth, attack, profile
    from app.api import api_blueprint
    from app.models import user, army

    app.register_blueprint(base.base, url_prefix="/base")
    app.register_blueprint(shop.shop, url_prefix="/shop")
    app.register_blueprint(auth.auth, url_prefix="/auth")
    app.register_blueprint(attack.attack, url_prefix="/attack")
    app.register_blueprint(profile.profile, url_prefix="/profile")
    app.register_blueprint(google_auth.google_auth, url_prefix="/google")
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must login to view this page')
    return redirect(url_for('auth.login', next=request.endpoint))
