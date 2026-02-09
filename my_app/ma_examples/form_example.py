from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

app = Flask(__name__)
app.secret_key = "your-secret-key-here"


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Пароль", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Подтвердите пароль", validators=[
        DataRequired(),
        EqualTo('password', message="Пароли должны совпадать")
    ])


@app.route("/", methods=["GET"])
def auth():

    login_form = LoginForm()
    register_form = RegisterForm()
    return render_template("index.html", login_form=login_form, register_form=register_form)


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        if username == "admin" and password == "12345678":
            flash("Вы успешно вошли!", "success")
        else:
            flash("Неверное имя пользователя или пароль", "error")

            register_form = RegisterForm()
            return render_template("index.html", login_form=form, register_form=register_form)

        return redirect(url_for('auth'))

    register_form = RegisterForm()
    return render_template("index.html", login_form=form, register_form=register_form)


@app.route("/register", methods=["POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        flash(f"Пользователь {username} успешно зарегистрирован!", "success")
        return redirect(url_for('auth'))

    login_form = LoginForm()
    return render_template("index.html", login_form=login_form, register_form=form)


if __name__ == '__main__':
    app.run(debug=True)