from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ======================
# TODO TABLE
# ======================
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# ======================
# DIARY TABLE
# ======================
class Diary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# ======================
# HOME PAGE
# ======================
@app.route('/', methods=['GET','POST'])
def home():

    if request.method == "POST":

        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)

        db.session.add(todo)
        db.session.commit()

        return redirect("/")

    allTodo = Todo.query.all()
    notes = Diary.query.order_by(Diary.date_created.desc()).all()

    return render_template("index.html", allTodo=allTodo, notes=notes)


# ======================
# DELETE TODO
# ======================
@app.route("/delete/<int:sno>")
def delete(sno):

    todo = Todo.query.filter_by(sno=sno).first()

    db.session.delete(todo)
    db.session.commit()

    return redirect("/")


# ======================
# COMPLETE TODO
# ======================
@app.route("/complete/<int:sno>")
def complete(sno):

    todo = Todo.query.filter_by(sno=sno).first()

    todo.completed = not todo.completed

    db.session.commit()

    return redirect("/")


# ======================
# UPDATE TODO
# ======================
@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):

    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == "POST":

        todo.title = request.form['title']
        todo.desc = request.form['desc']

        db.session.commit()

        return redirect("/")

    return render_template("update.html", todo=todo)


# ======================
# DIARY PAGE
# ======================
@app.route("/diary", methods=['POST'])
def diary():

    note = request.form['note']

    new_note = Diary(note=note)

    db.session.add(new_note)
    db.session.commit()

    return redirect("/")


# ======================
# SEARCH
# ======================
@app.route("/search")
def search():

    keyword = request.args.get("q")

    results = Todo.query.filter(Todo.title.contains(keyword)).all()
    notes = Diary.query.all()

    return render_template("index.html", allTodo=results, notes=notes)


# ======================
# LOGIN PAGE
# ======================
@app.route("/login")
def login():
    return render_template("login.html")


# ======================
# ABOUT PAGE
# ======================
@app.route("/about")
def about():
    return render_template("about.html")


# ======================
# CREATE DATABASE
# ======================
with app.app_context():
    db.create_all()


# ======================
# RUN APP
# ======================
if __name__ == "__main__":
    app.run(debug=True, port=8000)
