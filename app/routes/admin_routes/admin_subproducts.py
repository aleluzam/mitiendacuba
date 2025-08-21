from flask import Blueprint, request, jsonify
from app.models.subproducts_models import SubproductTable, SubproductCreate, SubproductUpdate
from app.models.products_models import ProductTable
from app.database import db
from pydantic import ValidationError
from app.dependencies import update_product_from_subproducts

admin_subproducts_bp = Blueprint("subproducts", __name__, url_prefix="/admin")



# MOSTRAR TODOS LOS SUBPRODUCTOS
@admin_subproducts_bp.route("/all_subproducts", methods=["GET"])
def all_subproducts():
    subproducts = db.session.query(SubproductTable).all()
    return jsonify ([p.to_dict() for p in subproducts])



# MOSTRAR SUBPRODUCTO POR ID (ADMIN)
@admin_subproducts_bp.route("/subproduct/<subproduct_id>", methods = ["GET"])
def get_subproduct(subproduct_id):
    try:
        subproduct = db.session.query(SubproductTable).filter(SubproductTable.subproduct_id == subproduct_id).first()
        if not subproduct:
            return jsonify({"error": f"Subproducto de id {subproduct_id} no encontrada"}), 404 
        return jsonify(subproduct.to_dict())   
    except Exception as e:
        return jsonify ({"mensaje": "Error interno del servidor",
                        "error": str(e)}), 500
    
# MOSTRAR VARIOS SUBPRODUCTOS POR PRODUCT_ID (ADMIN)
@admin_subproducts_bp.route("/subproducts/<product_id>", methods = ["GET"])
def get_subproducts_for_product(product_id):
    try:
        verify_product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if not verify_product:
            return jsonify ({"mensaje": f"No existe producto con id {product_id}"})
        
        subproducts = db.session.query(SubproductTable).filter(SubproductTable.product_id == product_id).all()
        if not subproducts:
            return jsonify ({"mensaje": f"El producto de id {product_id} no tiene subproductos"}), 404
        
        return jsonify([p.to_dict() for p in subproducts])
    except Exception as e:
        return jsonify ({"mensaje": "Error interno del servidor",
                        "error": str(e)}), 500
        
        

# CREAR SUBPRODUCTO
@admin_subproducts_bp.route("/subproduct/create", methods = ["POST"])
def create_subproduct():
    try:
        data = SubproductCreate.model_validate(request.get_json())
        verify_product_true = db.session.query(ProductTable).filter(ProductTable.product_id == data.product_id, ProductTable.subproducts.is_(True)).first()
        if not verify_product_true:
            return jsonify ({"mensaje": f"El producto de id {data.product_id} no esta habilitado para subproductos. Verifique e intente de nuevo"}), 400
        
        new_subproduct = SubproductTable(
            sub_name = data.sub_name,
            sub_description = data.sub_description,
            sub_stock = data.sub_stock,
            product_id = data.product_id
        )       
        db.session.add(new_subproduct)
        db.session.commit()
        update_product_from_subproducts(new_subproduct.product_id)
        return jsonify({
            "mensaje": "Subproducto creado satisfactoriamente",
            "subproducto": {
                "subproduct_id": new_subproduct.subproduct_id,
                "sub_name": new_subproduct.sub_name,
                "sub_description": new_subproduct.sub_description,
                "sub_stock": new_subproduct.sub_stock,
                "product_id": new_subproduct.product_id
            }})
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



# EDITAR SUBPRODUCTO
@admin_subproducts_bp.route("/subproduct/edit/<subproduct_id>", methods = ["PUT", "PATCH"])
def edit_subproduct(subproduct_id):
    try:
        data = SubproductUpdate.model_validate(request.get_json())
        verify_new_product_id = db.session.query(ProductTable).filter(ProductTable.product_id == data.product_id, ProductTable.subproducts.is_(True)).first()
        if not verify_new_product_id:
            return jsonify ({"mensaje": f"El id {data.product_id} pertenece a un producto no habilitado para subproductos"}), 400
        to_edit = db.session.query(SubproductTable).filter(SubproductTable.subproduct_id == subproduct_id).first()
        if not to_edit:
            return jsonify ({"mensaje": f"No encontrado subproducto de id {subproduct_id}"}), 404
        old_id = to_edit.product_id # id de producto que puede abandonar el subproducto
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(to_edit, field, value)
        db.session.commit()
        update_product_from_subproducts(to_edit.product_id)
        update_product_from_subproducts(old_id) # si el subproducto abandona algun producto
        return jsonify ({
                "mensaje": f"El subproducto de id {subproduct_id} ha sido editado correctamente",
                "subproducto": {
                    "product_id": to_edit.product_id,
                    "sub_name": to_edit.sub_name,
                    "sub_description": to_edit.sub_description,
                    "sub_stock": to_edit.sub_stock,
                }})  
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

