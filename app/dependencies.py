from app.database import db
from flask import jsonify, request
from app.models.products_models import ProductTable
from app.models.subproducts_models import SubproductTable
from sqlalchemy import func
import jwt
from dotenv import load_dotenv
import os
import secrets

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")



# Calcular el stock total de producto sumando subproductos
def update_product_from_subproducts(product_id):
    try:
        total_stock_subproduct = db.session.query(func.sum(SubproductTable.sub_stock)).filter(SubproductTable.product_id == product_id).scalar()
        if total_stock_subproduct is None:
            total_stock_subproduct = 0
        product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if not product:
            raise ValueError(f"Producto de id {product_id} no encontrado")
        else:
            product.stock = total_stock_subproduct
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e    
    


# OBTENER ID DE TOKEN DE USUARIO AUTENTICADO
def get_id_from_jwt():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        return user_id
    
    except Exception as e:
        return None
    
# GENERAR UN NUMERO DE 6 DIGITOS RANDOMS
def generate_reset_code():
    return secrets.randbelow(900000) + 100000
       

def validate_image_file(file):
    """
    Valida un archivo de imagen
    Returns: dict con 'valid' (bool) y 'error' (str si hay error)
    """
    
    if not file or file.filename == "":
        return {"valid": False, "error": "Archivo vacío"}
    
    allowed_extensions = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "tiff"}
    file_extension = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else ""
    
    if file_extension not in allowed_extensions:
        return {"valid": False, "error": f"Extensión no permitida. Formatos permitidos: {', '.join(allowed_extensions)}"}
    
    allowed_mimes = [
        'image/jpeg', 'image/png', 'image/gif', 
        'image/webp', 'image/bmp', 'image/tiff'
    ]
        
    if file.content_type not in allowed_mimes:
        return {
            'valid': False, 
            'error': f'Tipo de archivo no válido. Recibido: {file.content_type}'
        }
    
    # Obtener tamaño del archivo
    file.seek(0, 2)  
    file_size = file.tell() 
    file.seek(0)  
    
    min_size = 1024  # 1KB
    if file_size < min_size:
        return {'valid': False, 'error': 'Archivo muy pequeño (mínimo 1KB)'}
    
    max_size = 10 * 1024 * 1024  # 10MB
    if file_size > max_size:
        return {
            'valid': False, 
            'error': f'Archivo muy grande. Máximo {max_size//1024//1024}MB, recibido {file_size//1024//1024}MB'
        }
    
    # Validar que sea una imagen válida
    try:
        from PIL import Image
        
        file.seek(0)
        img = Image.open(file)
        img.verify() 
        file.seek(0) 
        
        if img.width < 10 or img.height < 10:
            return {'valid': False, 'error': 'Imagen muy pequeña (mínimo 10x10 píxeles)'}
        
        if img.width > 5000 or img.height > 5000:
            return {'valid': False, 'error': 'Imagen muy grande (máximo 5000x5000 píxeles)'}
            
    except Exception as e:
        return {'valid': False, 'error': 'El archivo no es una imagen válida'}
    
    return {"valid": True} 