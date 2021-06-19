from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User


@app.route("/")
def hello_world():
    return render_template("index.html", users=User.get_all())


@app.route("/create_user", methods=["POST"])
def create_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
    }
    User.save(data)
    return redirect("/")


@app.route("/edit_page/<int:id>")
def edit_page(id):
    data = {"id": id}
    return render_template("edit_page.html", user=User.get_one(data))


@app.route("/update_user/<int:id>", methods=["POST"])
def update_user(id):
    data = {
        "id": id,
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
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