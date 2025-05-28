from flask import Flask, jsonify, Blueprint
from dotenv import load_dotenv 
from database import get_mysql_uri
from database import db
from sqlalchemy import Integer
from models.products_models import Product
from models.users import UserTable
from routes.admin_users import users_bp
from routes.admin_products import products_bp

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

#Exportando los Blueprints
app.register_blueprint(users_bp)
app.register_blueprint(products_bp)


db.init_app(app) # inicia la conexion con la base de datos

# Crear las tablas
with app.app_context():
    db.create_all() # crea las tablas de las clases que hereden db.Model y que esten importadas

@app.route("/")
def hello():
    return jsonify({"Message": "Bienvenido a MiTiendaCuba"}) 


if __name__ == '__main__':
    app.run(debug=True)

"""
Para subir a git

git init
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/0rdan/mitiendacuba.git
push -u origin main 
 """