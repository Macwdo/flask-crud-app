from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI
import sqlite3


api = FastAPI()
db = SQLAlchemy()
app =  Flask('__name__',template_folder="templates")
#Data base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///livros.sqlite3"
con = sqlite3.connect("instance/livros.sqlite3",check_same_thread=False)
dbcursor = con.cursor()


class Livros(db.Model):
    id = db.Column('id',db.Integer,primary_key=True,autoincrement=True)
    titulo = db.Column(db.String(30))
    autor = db.Column(db.String(30))
    
    def __init__(self,titulo,autor):
        self.titulo = titulo
        self.autor = autor
        
@app.route('/<int:id>',methods=["GET"])
def livro(id):
    livros = db.get_or_404(Livros,id)
    return render_template("view.html",livro=livros)


@app.route('/list')
def list():
    livros = Livros.query.all()
    return render_template("list.html",livros=livros)

@app.route('/',methods=['POST','GET'])
def create():
    if request.method == "POST":
        livro = Livros(autor=request.form["autor"],titulo=request.form["titulo"])
        db.session.add(livro)
        db.session.commit()
        return redirect(url_for("list"))
    if request.method == "GET":
        return render_template("create.html")
    
    
@app.route('/delete/<int:id>',methods=['GET'])
def delete(id):
    if request.method == "GET":
        livro = db.get_or_404(Livros,id)
        db.session.delete(livro)
        db.session.commit()
        return redirect(url_for("list"))

@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method == "GET":
        livro = Livros.query.get(id)
        return render_template("update.html",livro=livro)
    if request.method == "POST":
        livro = Livros.query.get(id)
        livro.titulo = request.form["titulo"]
        livro.autor = request.form["autor"]
        db.session.commit()
        return redirect(url_for("list"))


@api.get("/api")
async def list_view_api():
    dbcursor.execute(f"SELECT id, titulo, autor FROM Livros")
    dados = []
    resultado = dbcursor.fetchall()
    for dado in resultado:
        serializer = {
            "id": dado[0],
            "titulo": dado[1],
            "autor": dado[2]
        }
        dados.append(serializer)
    return dados

@api.post("/api")
async def list_view_api(titulo: str, autor:str):
    dbcursor.execute(f"INSERT INTO Livros (titulo, autor) VALUES ({titulo},{autor})")
    dados = []
    resultado = dbcursor.fetchall()
    for dado in resultado:
        serializer = {
            "id": dado[0],
            "titulo": dado[1],
            "autor": dado[2]
        }
        dados.append()

@api.get("/api/{id}")
async def view_api(id: int):
    dbcursor.execute(f"SELECT id, titulo, autor FROM Livros WHERE id={id}")
    dados = dbcursor.fetchone()
    return {
        'id':dados[0],
        'titulo':dados[1],
        'autor':dados[2]
        }

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
