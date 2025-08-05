from app.models.sales_models import SaleTable, ItemsTable
from flask import jsonify, request, Blueprint
from app.database import db
from datetime import datetime, UTC, timezone
from zoneinfo import ZoneInfo
from app.models.products_models import ProductTable
from app.models.subproducts_models import SubproductTable
from app.dependencies import update_product_from_subproducts

admin_sales_bp = Blueprint("admin_sales", __name__, url_prefix=("/admin"))

cuba_tz = ZoneInfo('America/Havana')

# VER TODAS LAS VENTAS CON RESPECTIVOS ITEMS (ADMIN)
@admin_sales_bp.route("/all_sales",methods = ["GET"])
def get_all_sales():
    try: 
        sales = db.session.query(SaleTable).all()
        return jsonify ([s.to_all() for s in sales])
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# PROCESAR VENTAS
@admin_sales_bp.route("/new_sale", methods = ["POST"])
def new_sale():
    data = request.get_json()
    if not data:
        return jsonify ({"error": "Datos de compra requeridos"}), 400
    user_id = data.get("user_id")
    if not user_id:
        return jsonify ({"error": "ID de comprador requerida"}), 400
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