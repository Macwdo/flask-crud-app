from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app =  Flask('__name__')
#Data base
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

db.session

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)