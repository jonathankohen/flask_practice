from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.friend import Friend
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def hello_world():
    return render_template("index.html", users=User.get_all())


@app.route("/register", methods=["POST"])
def register():
    if not User.validate_reg(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash("This email is already in our database. Please sign in!")
        return redirect("/")

    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid credentials.")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid credentials.")
        return redirect("/")
    session["user_id"] = user_in_db.id
    print(session["user_id"])
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/edit_page/<int:id>")
def edit_page(id):
    data = {"id": id}
    return render_template("edit_page.html", user=User.get_user_with_friends(data))


@app.route("/user/add_friend/<int:user_id>", methods=["POST"])
def add_friend(user_id):
    data = {"user_id": user_id, "nickname": request.form["nickname"]}
    Friend.save(data)
    return redirect("/")


@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
    }
    User.update(data)
    return redirect("/")


@app.route("/delete_user/<int:id>")
def delete_user(id):
    data = {
        "id": id,
    }
    User.delete(data)
    return redirect("/")