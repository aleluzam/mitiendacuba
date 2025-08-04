from flask import Blueprint, jsonify, request
from database import db
from models.products_models import ProductTable, ProductCreate, ProductUpdate
from models.subproducts_models import SubproductTable
from security import login_required
from dependencies import update_product_from_subproducts
from pydantic import ValidationError
from routes.admin_routes.admin_alerts import stock_alerts

admin_products_bp = Blueprint("admin_products", __name__, url_prefix="/admin")



### PRODUCTOS ###



# MOSTRAR TODOS LOS PRODUCTOS (ADMIN)
@admin_products_bp.route('/all_products', methods=["GET"])
def get_products():
    products = db.session.query(ProductTable).all()  
    return jsonify([p.to_dict() for p in products])



# MOSTRAR PRODUCTO POR ID (ADMIN)
@admin_products_bp.route("/product/<data_id>", methods=["GET"])
def get_product(data_id):
        product = db.session.query(ProductTable).filter(ProductTable.product_id == data_id).first()
        if not product:
            return jsonify({"error": "ID incorrecta"}), 400
        else:
            return jsonify(product.to_dict())
        
        
        
# CREAR PRODUCTO (ADMIN)
@admin_products_bp.route("/product/create", methods=["POST"])
def create_product():
    try:
        # Validar datos de entrada
        data = ProductCreate.model_validate(request.get_json())
        
        # Crear objeto SQLAlchemy (no dict)
        new_product = ProductTable(  
            name = data.name,          
            price = data.price,
            description = data.description,
            stock = data.stock,
            subproducts = data.subproducts,
            limit_stock = int(data.stock * 0.1),
            section = data.section  
        )   
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "message": "Producto creado satisfactoriamente",
            "product": {
                "id": new_product.product_id,
                "name": new_product.name,
                "price": new_product.price,
                "description": new_product.description,
                "stock": new_product.stock,
                "section": new_product.section
            }
        }), 201  
        
    except ValidationError as e:
        # Error de validación de Pydantic
        return jsonify({
            "error": "Datos inválidos",
            "details": [{"field": err['loc'][0], "message": err['msg']} 
                       for err in e.errors()]
        }), 400 

    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        
        
        
# EDITAR PRODUCTO (ADMIN)
@admin_products_bp.route("/product/edit/<product_id>", methods = ["PUT", "PATCH"])
def edit_product(product_id):
    try:
        data = ProductUpdate.model_validate(request.get_json()) # no se verifica aqui porque se hace en el except
        
        to_edit = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if not to_edit:
            return jsonify ({"error": f"Producto de id {product_id} no encotrado"}), 404
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(to_edit, field, value)
        
        db.session.commit()
        return jsonify({
            "mensaje": f"El producto de id {product_id} ha sido editado correctamente",
            "producto": {
                "product_id": to_edit.product_id,
                "name": to_edit.name,
                "price": to_edit.price,
                "description": to_edit.description,
                "stock": to_edit.stock,
                "subproducts": to_edit.subproducts,
                "section": to_edit.section
            }
})    
    except ValidationError as e:
        return jsonify({
            "error": "Datos inválidos",
            "details": [{"field": err['loc'][0], "message": err['msg']} 
                       for err in e.errors()]
        }), 400 
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        
        
           
# ELIMINAR PRODUCTO Y SUBPRODUCTOS POR ID (ADMIN)
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
    
    
    
### PRODUCTOS DESTACADOS ###



# VER PRODUCTOS DESTACADOS
@admin_products_bp.route("/featured_products/all", methods = ["GET"])
def get_all_featured_products():
    featured_products = db.session.query(ProductTable).filter(ProductTable.featured == True).all()
    if not featured_products :
        return jsonify({"message": "No hay productos destacados actualmente"})
    
    try:
        return jsonify([p.to_dict() for p in featured_products])
     
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500



# CONVERTIR PRODUCTO A DESTACADO (ID)
@admin_products_bp.route("/featured_products/to_featured/<product_id>", methods = ["PUT"])
def turn_featured(product_id):
    product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
    if not product:
        return jsonify({"message": "No existe producto con esta id"}), 404
    
    try:
        product.featured = True
        db.session.commit()
        return jsonify ({"message": "Producto convertido a destacado exitosamente"})
        
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500



# CONVERTIR PRODUCTO A REGULAR (ID)
@admin_products_bp.route("/featured_products/to_regular/<product_id>", methods = ["PUT"])
def turn_regular(product_id):
    product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
    if not product:
        return jsonify({"message": "No existe producto con esta id"}), 404
    
    try:
        product.featured = False
        db.session.commit()
        return jsonify ({"message": "Producto convertido a regular exitosamente"})
        
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        

    