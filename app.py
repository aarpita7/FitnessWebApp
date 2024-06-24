from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()

db.init_app(app)
# @app.before_first_request
# def create_table():
#     db.create_all()

class Users(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String)
    password = db.Column(db.String)
    uemail = db.Column(db.String)
    uphone = db.Column(db.String)
    city = db.Column(db.String)
    gender = db.Column(db.String)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    profile = relationship('Profile', back_populates='user')
    posts = relationship('Posts', back_populates='user')
    udata = relationship('UserData', back_populates='user')
    agenda = relationship('Agenda', back_populates='user')
    explore = relationship('Explore', back_populates='user')
    message = relationship('Message', back_populates='user')

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/Dashboard.html')
def dashboard():
    return render_template('Dashboard.html')

@app.route('/agenda.html')
def agenda():
    return render_template('agenda.html')

@app.route('/explore.html')
def explore():
    return render_template('explore.html')

# @login_manager.user_loader
# def loader_user(uid):
#     return Users.query.get(uid)

@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = Users(uname=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            uname=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
