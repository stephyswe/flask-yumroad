from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user


from yumroad.email import send_pretty_welcome_message
from yumroad.extensions import login_manager
from yumroad.forms import LoginForm, SignupForm
from yumroad.models import Store, User, db

user_bp = Blueprint("user", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    session["after_login"] = request.url
    return redirect(url_for("user.login"))


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("product.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for("product.index"))

    return render_template("users/login.html", form=form)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in", "warning")
        return redirect(url_for("product.index"))

    form = SignupForm()
    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        store = Store(name=form.store_name.data, user=user)
        db.session.add(user)
        db.session.add(store)
        db.session.commit()

        send_pretty_welcome_message(user)
        login_user(user)
        flash("Registered successfully.", "success")
        return redirect(session.get("after_login") or url_for("product.index"))
    return render_template("users/register.html", form=form)


@user_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("product.index"))
    # You may want to only allow access through a POST request
