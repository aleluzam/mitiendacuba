from flask_mail import Message
from flask import current_app, jsonify, Blueprint
import threading

# FUNCION AUXILIAR - ARREGLADA para recibir 3 parámetros
def send_mail_async(app, mail_instance, msg):
    with app.app_context():
        mail_instance.send(msg)

def send_mail(email, html_body=None):
    try:
        mail_instance = current_app.extensions['mail']
        
        msg = Message(
            subject="Codigo para regenerar password",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email]
        )
        msg.body = f"Tu codigo de reestablecimiento es"
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

