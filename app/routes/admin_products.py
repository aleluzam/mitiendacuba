from flask import Blueprint, jsonify
from database import db
from models.products_models import ProductTable
from models.subproducts_models import SubproductTable
from security import login_required

admin_products_bp = Blueprint("products", __name__, url_prefix="/admin")


# PRODUCTOS

# Mostrar todos los productos (para admin)
@admin_products_bp.route('/all_products', methods=["GET"])
def get_products():
    products = db.session.query(ProductTable).all()  
    return jsonify([p.to_dict() for p in products])

#Mostrar producto por id (para admin)
@admin_products_bp.route("/product/<data_id>", methods=["GET"])
def get_product(data_id):
        product = db.session.query(ProductTable).filter(ProductTable.product_id == data_id).first()
        if not product:
            return jsonify({"error": "ID incorrecta"}), 400
        else:
            return jsonify(product.to_dict())

#Eliminar producto por id, junto a subproductos
@admin_products_bp.route("/product/delete/<data_id>", methods=["DELETE"])
def delete_product(data_id):
    product = db.session.query(ProductTable).filter(ProductTable.product_id == data_id).first()
    if not product:
            return jsonify ({"error": "ID de producto incorrecta"}), 404
    try:       
        if product.subproducts == True:
            subproducts = db.session.query(SubproductTable).filter(SubproductTable.product_id == data_id).all() 
            try:
                for sp in subproducts:
                    db.session.delete(sp)
                db.session.flush()
            except:
                db.session.rollback()
                return jsonify ({"error": "Error eliminando subproductos"}), 500
     
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"El producto de ID {data_id} y sus subproductos han sido eliminados"})
    except:
        db.session.rollback()
        return jsonify ({"error": "Error al eliminar producto"}), 500
            
        
        

        



# SUBPRODUCTOS

# Mostrar todos los subproductos
@admin_products_bp.route("/all_subproducts", methods=["GET"])
def all_subproducts():
    subproducts = db.session.query(SubproductTable).all()
    return jsonify ([p.to_dict() for p in subproducts])