from database import db
from flask import jsonify, request
from models.products_models import ProductTable
from models.subproducts_models import SubproductTable
from sqlalchemy import func

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
    
            
    

    
    
    