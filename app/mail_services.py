from flask_mail import Message
from flask import current_app, jsonify, Blueprint
import threading

mail_bp = Blueprint("mail", __name__, url_prefix=("/mail"))

# FUNCION AUXILIAR - ARREGLADA para recibir 3 parámetros
def send_mail_async(app, mail_instance, msg):
    with app.app_context():
        mail_instance.send(msg)

def send_mail(email, html_body=None):
    try:
        
        mail_instance = current_app.extensions['mail']
        
        msg = Message(
            subject="Aqui ira el codigo",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.body = "Tu codigo ira aqui"
        if html_body:
            msg.html = html_body
        
        thread = threading.Thread(
            target=send_mail_async,
            args=(current_app._get_current_object(), mail_instance, msg)
        )
        thread.start()
        
        return {"success": True, "codigo": "aqui ira el codigo"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}    

@mail_bp.route("/mail", methods=["GET"])
def test_mail():
    try:
        test_mail = "milymaciasfernandez@gmail.com"
        resultado = send_mail(
            email=test_mail,
            html_body="<h2>TE AMO MI AMORCITO</h2><p>Estoy pa darte en una pila de partes</p>"
        )
        return jsonify({
            "success": True, 
            "message": f"Correo de prueba enviado a {test_mail}",
            "resultado": resultado
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "message": f"Error al enviar correo de prueba: {str(e)}"
        })
