from flask import Blueprint, jsonify, request
import cloudinary
import cloudinary.uploader
from app.dependencies import validate_image_file

img_manager_bp = Blueprint("img_manager", __name__, url_prefix="/admin/image_manager")


@img_manager_bp.route("/upload_image", methods = ["POST"])
def upload_img():
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "error": "No se envio ningun archivo"}), 400
        
        file = request.files["image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "No se selecciono archivo"}), 400
        
        validation_result = validate_image_file(file)
        if not validation_result["valid"]:
            return jsonify({"success": False, "error": validation_result["error"]}), 400
        
        result = cloudinary.uploader.upload(
            file,
            public_id = file.filename,
            width = 1200,
            height = 800,
            crop = 'limit',
            quality = 'auto:good'
        )
        
        return jsonify({
            "success": True,
            "message": "Imagen subida exitosamente",
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "width": result.get("width"),
            "height": result.get("height"),
            "format": result.get("format"),
            "bytes": result.get("bytes")
        }), 200
        
    except Exception as e:
        print(f"Error subiendo imagen: {str(e)}")
        print(f"Tipo de error: {type(e).__name__}")
        
        return jsonify({
            "success": False, 
            "error": "Error interno del servidor al subir la imagen"
        }), 500
    
    
    
    
    
    
    
