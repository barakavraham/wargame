from flask import Flask, render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '827677ccbc5d49e567a7fceed8b43c26v4uh4hwp4gihr'


@app.route("/")
def base():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(debug=True)
