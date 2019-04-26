from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '827677ccbc5d49e567a7fceed8b43c26v4uh4hwp4gihr'


@app.route("/")
def base():
    return render_template('base.html')


@app.route("/shop")
def shop():
    return render_template('shop.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created: {form.username.data}')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login")
def login():
    # test test test test test test test test test test test test test
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
