from flask import Flask, jsonify
from dotenv import load_dotenv 
from database import get_mysql_uri, db
from routes.admin_routes.admin_users import admin_users_bp
from routes.admin_routes.admin_products import admin_products_bp
from routes.admin_routes.admin_subproducts import admin_subproducts_bp
from routes.admin_routes.admin_sales import admin_sales_bp
from routes.admin_routes.admin_notifications import admin_notifications_bp
from routes.auth import auth_bp
from routes.user_routes.user_products import user_products_bp
from routes.user_routes.user_users import user_users_bp
from routes.user_routes.user_sales import user_sales_bp
<<<<<<< HEAD
from mail_services import mail_bp
from flask_mail import Mail, Message
import os

=======
>>>>>>> c037a7696cf69cd473c9a034f71011fc11f43ed0
load_dotenv()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# CONFIGURACIONES DEL CORREO
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', "True").lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', "False").lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)

#Registar los Blueprints
app.register_blueprint(admin_users_bp)                                                                                                                                                                                                                                                                                                                                                                                                                      
app.register_blueprint(admin_products_bp)
app.register_blueprint(admin_subproducts_bp)
app.register_blueprint(admin_sales_bp)
app.register_blueprint(admin_notifications_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_products_bp)
app.register_blueprint(user_users_bp)
app.register_blueprint(user_sales_bp)
<<<<<<< HEAD
app.register_blueprint(mail_bp)
=======
>>>>>>> c037a7696cf69cd473c9a034f71011fc11f43ed0


db.init_app(app) # inicia la conexion con la base de datos

# Crear las tablas
with app.app_context():
    db.create_all() # crea las tablas de las clases que hereden db.Model y que esten importadas

@app.route("/")
def hello():
    return jsonify({"Message": "Bienvenido a MiTiendaCuba"}) 


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug=True)



