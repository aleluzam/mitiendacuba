from flask import Flask, jsonify
from dotenv import load_dotenv 
from database import get_mysql_uri, db
from routes.admin_routes.admin_users import admin_users_bp
from routes.admin_routes.admin_products import admin_products_bp
from routes.admin_routes.admin_subproducts import admin_subproducts_bp
from routes.auth import auth_bp
from routes.user_routes.user_products import user_products_bp
from routes.user_routes.user_users import user_users_bp
from routes.admin_routes.admin_sales import admin_sales_bp

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  

#Registar los Blueprints
app.register_blueprint(admin_users_bp)                                                                                                                                                                                                                                                                                                                                                                                                                      
app.register_blueprint(admin_products_bp)
app.register_blueprint(admin_subproducts_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_products_bp)
app.register_blueprint(user_users_bp)
app.register_blueprint(admin_sales_bp)



db.init_app(app) # inicia la conexion con la base de datos

# Crear las tablas
with app.app_context():
    db.create_all() # crea las tablas de las clases que hereden db.Model y que esten importadas

@app.route("/")
def hello():
    return jsonify({"Message": "Bienvenido a MiTiendaCuba"}) 


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True)



