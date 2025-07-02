from database import db
from flask import jsonify, request
from models.products_models import ProductTable
from models.subproducts_models import SubproductTable
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
       
            
    

    
    
    