from database import db
from flask import jsonify, Blueprint, request
from models.codes_models import CodeTable
from dependencies import generate_reset_code
from mail_services import send_mail, send_mail_async
from models.users_models import UserTable
from datetime import datetime, timezone, tzinfo

mail_codes_bp = Blueprint("codes", __name__, url_prefix= ("/auth"))

# VER TODOS LOS CODIGOS
@mail_codes_bp.route("/all_codes", methods = ["GET"])
def get_all_codes():
    codes = db.session.query(CodeTable).all()
    return jsonify ([p.to_admin() for p in codes])



# VERIFICAR SI EL MAIL INTRODUCIDO ES CORRECTO, ENVIAR EL CODIGO Y ALMACENARLO
@mail_codes_bp.route("/send_code", methods=["POST"])
def verify_mail_and_send_code():
    data_mail = request.get_json()
    if not data_mail:
        return jsonify ({"error": "Correo requerido"}), 400
    try:
        data_mail = data_mail["mail"]
        verify_mail = db.session.query(UserTable).filter(UserTable.mail == data_mail).first()
        if not verify_mail: 
            return jsonify ({"error": "Correo no encontrado"}), 404
        
        code = generate_reset_code()
        
        resultado = send_mail(
            email = data_mail,
            html_body=f"<h2>CODIGO PARA RESTABLECER PASSWORD</h2><p>Tu codigo es {code}</p>"
        )
        
        new_code = CodeTable(
            code = code,
            user_id = verify_mail.user_id
        )
        db.session.add(new_code)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Correo enviado a {data_mail}"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False, 
            "message": f"Error al enviar correo de prueba: {str(e)}"
        })


# VERIFICAR SI EL CODIGO ES CORRECTO
@mail_codes_bp.route("/verify_code", methods = ["POST"])
def verify_code():
    code = request.get_json()
    if not code or "code" not in code:
        return jsonify({"valid": False, 
                        "error": "Codigo requerido"}), 400
    try:
        code = code["code"]
        verify_code = db.session.query(CodeTable).filter(CodeTable.code == code, CodeTable.used == False).first()
        if not verify_code:
            return jsonify ({"valid": False,
                             "error": "Codigo inexistente o usado"}), 404
        current_time = datetime.now(timezone.utc)
        expires_at = verify_code.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo = timezone.utc)   
        if current_time > expires_at:
            return jsonify ({"valid": False,
                             "error": "Codigo expirado"}), 410 # GONE expirado
        verify_code.used = True
        db.session.commit()
        return jsonify ({"valid": True,
                         "message": "Codigo valido"})
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "valid": False, 
            "message": f"Error: {str(e)}"
        }), 500
        
        

# END DE PRUEBA
@mail_codes_bp.route("/test", methods = ["POST"])
def test_mail():
    try:
        code = generate_reset_code()
        mail = "alzzla2004@gmail.com"
        user_mail = db.session.query(UserTable).filter(UserTable.mail == mail).first()
        
        resultado = send_mail(
            email = mail,
            html_body=f"<h2>CODIGO PARA RESTABLECER PASSWORD</h2><p>Tu codigo es {code}</p>"
        )
        
        new_code = CodeTable(
            code = code,
            user_id = user_mail.user_id
        )
        db.session.add(new_code)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Correo de prueba enviado a {mail}"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False, 
            "message": f"Error al enviar correo de prueba: {str(e)}"
        })

        
        
        