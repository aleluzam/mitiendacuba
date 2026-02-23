from flask import Flask, Blueprint, jsonify, request
from database import db
from dependencies import get_id_from_jwt
from models.sales_models import SaleTable
from models.subproducts_models import SubproductTable
from models.products_models import ProductTable
from models.sales_models import ItemsTable
from zoneinfo import ZoneInfo
from datetime import datetime
from dependencies import update_product_from_subproducts

cuba_tz = ZoneInfo('America/Havana')


user_sales_bp = Blueprint("user_sales", __name__, url_prefix=("/user"))

# Ver mi historial de compras
@user_sales_bp.route("/my_profile/my_purchases", methods = ["GET"])
def get_my_purchases():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify({"error": "Token requerido o invalido"}), 401
    try:
        purchases = db.session.query(SaleTable).filter(SaleTable.user_id == user_id).all()
        if not purchases:
            return jsonify ({"mensaje": "Su historial de compras esta vacio"})
        return jsonify ([s.to_user() for s in purchases])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500


# PROCESAR VENTAS
@user_sales_bp.route("/sales/new", methods = ["POST"])
def new_sale():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token requerido o invalido"}), 401

    data = request.get_json()
    if not data:
        return jsonify ({"error": "Datos de compra requeridos"}), 400
    items = data.get("items", [])
    if not items:
        return jsonify ({"error": "No hay productos a la venta"}), 400
    try: 
        new_sale = SaleTable(
            user_id = user_id,
            created_at = datetime.now(cuba_tz),
            total_amount = 0
            )
        db.session.add(new_sale)
        db.session.flush() # para que se cree el sale_id
        
        to_public_items = []
        total_sale = 0
        # HASTA AQUI NO AGREGAR NADA DE SUBPRODUCTOS
        for p in items:
            
            subproduct = None
            
            product_id = p.get("product_id")
            quantity = p.get("quantity")
            if "subproduct_id" in p:
                subproduct_id = p.get("subproduct_id")
                subproduct = db.session.query(SubproductTable).filter(SubproductTable.subproduct_id == subproduct_id).first()
                if not subproduct:
                    return jsonify ({"error": f"El subproducto de id {subproduct_id} no fue encontrado"}), 404 
            product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
            if not product:
                return jsonify ({"error": f"El producto de id {product_id} no fue encontrado"}), 404
            
            if subproduct:
                if subproduct.sub_stock < quantity:
                    return jsonify ({"error": f"Stock insuficiente para subproducto de id {subproduct_id}"}), 400
            else:
                if product.stock < quantity:
                    return jsonify ({"error": f"Stock insuficiente para producto de id {product_id}"}), 400
    
            total_price = quantity * product.price
            total_sale += total_price
            
            item = ItemsTable(
                sale_id = new_sale.sale_id,
                product_id = product_id,
                product_name = product.name,
                sub_name = subproduct.sub_name if subproduct else None,
                product_price = product.price,
                quantity = quantity,
                total_amount = total_price
            )
            db.session.add(item)
            to_public_items.append(item)
            
            if subproduct:
                db.session.query(SubproductTable).filter(SubproductTable.subproduct_id == subproduct_id).update({SubproductTable.sub_stock: SubproductTable.sub_stock - quantity })
                update_product_from_subproducts(product_id)
            else:
                db.session.query(ProductTable).filter(ProductTable.product_id == product_id).update({ProductTable.stock: ProductTable.stock - quantity })
        
        db.session.query(SaleTable).filter(SaleTable.sale_id == new_sale.sale_id).update({SaleTable.total_amount: total_sale})
        db.session.commit()
        return jsonify ({
            "mensaje": "Venta creada exitosamente",
            "sale_id": new_sale.sale_id,
            "total": total_sale,
            "total_items": len(to_public_items),
            "items": [
                {
                "product_id": i.product_id,
                "product_name": i.product_name,
                "sub_name": i.sub_name,
                "quantity": i.quantity,
                "price": i.product_price,
                "subtotal": i.total_amount
                }
                for i in to_public_items
            ]
            }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500