from flask import Flask, redirect, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '827677ccbc5d49e567a7fceed8b43c2682c8469c2aa2b84d648349ef2fd7f4d0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must login to view this page')
    return redirect(url_for('auth.login', next=request.endpoint))


from app.routes import base, shop, auth, google_auth

app.register_blueprint(base.base, url_prefix="/base")
app.register_blueprint(shop.shop, url_prefix="/shop")
app.register_blueprint(auth.auth, url_prefix="/auth")
app.register_blueprint(google_auth.google_auth, url_prefix="/google")