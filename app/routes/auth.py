from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models.user import User
from app.forms.auth_forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


# -----------------------
# Register
# -----------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        role = "reader"
        if form.user_type.data == 'admin':
            if form.admin_key.data == current_app.config.get('ADMIN_REGISTRATION_KEY'):
                role = "admin"
            else:
                flash("Invalid admin registration key.", "danger")
                return render_template("signup.html", form=form)

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_pw,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)


# -----------------------
# Login
# -----------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        try:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash("Logged in successfully!", "success")
                # Respect `next` param when present (only allow relative URLs).
                # Use request.values so we accept next from querystring (GET) or
                # as a hidden form field (POST).
                next_page = request.values.get("next")
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for("main.home"))
        except ValueError:
            # bcrypt raised ValueError for invalid salt/format
            flash("Invalid email or password.", "danger")
            return render_template("login.html", form=form)

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


# -----------------------
# Logout
# -----------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("main.home"))
