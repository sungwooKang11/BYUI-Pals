from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

@app.route("/")
def index():
  return render_template("index.html")

# HOME
@app.route("/home")
def home():
  return render_template("index.html")

# GROUP
class Group(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.String(120), unique=True, nullable=False)

  def __repr__(self):
    return f"Group('{self.name}', '{self.description}')"

class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  comment = db.Column(db.String(80), unique=True, nullable=False)
  group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

  def __repr__(self):
    return f"Comments('{self.comment}', '{self.group_id}')"

@app.route("/group", methods=["GET", "POST"])
def group():
  if request.method == "POST":
    # Add a new group
    group = Group(
      name=request.form["name"],
      description=request.form["description"]
      )
    db.session.add(group)
    db.session.commit()
  return render_template("group.html")

@app.route("/group/<int:group_id>", methods=["GET", "POST"])
def group_detail(group_id):
  if request.method == "POST":
    # Add a new comment to the group
    comment = Comment(
      comment=request.form["comment"],
      group_id=request.form["group_id"]
      )
    db.session.add(comment)
    db.session.commit()
  group = Group.query.get(group_id)
  comments = Comment.query.filter_by(group_id=group_id).all()

  # Get the groups and their comments
  return render_template("group_detail.html", group=group, comments=comments)

# TRADE
@app.route("/trade")
def trade():
  return render_template("trade.html")

# CARPOOL
@app.route("/carpool")
def carpool():
  return render_template("carpool.html")

app.run(debug=True, port=5001)