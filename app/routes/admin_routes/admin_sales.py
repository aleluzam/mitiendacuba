from app.models.sales_models import SaleTable
from flask import jsonify, request, Blueprint
from app.database import db
from app.dependencies import update_product_from_subproducts

admin_sales_bp = Blueprint("admin_sales", __name__, url_prefix=("/admin"))


# VER TODAS LAS VENTAS CON RESPECTIVOS ITEMS (ADMIN)
@admin_sales_bp.route("/sales/all",methods = ["GET"])
def get_all_sales():
    try: 
        sales = db.session.query(SaleTable).all()
        return jsonify ([s.to_all() for s in sales])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
# VER VENTAS PENDIENTES DE COMPLETAR
@admin_sales_bp.route("/sales/pending_sales", methods = ["GET"])
def get_pending_sales():
    try: 
        sales = db.session.query(SaleTable).filter(SaleTable.completed == False).all()
        if not sales:
            return jsonify ({"message": "No hay ventas sin completar actualmente"})
        
        return jsonify ([s.to_all() for s in sales])
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# VER VENTAS COMPLETADAS
@admin_sales_bp.route("/sales/completed_sales", methods = ["GET"])
def get_completed_sales():
    try: 
        sales = db.session.query(SaleTable).filter(SaleTable.completed == True).all()
        if not sales:
            return jsonify ({"message": "No hay ventas completadas actualmente"})
        
        return jsonify ([s.to_all() for s in sales])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
# COMPLETAR UNA VENTA   
@admin_sales_bp.route("/sales/complete_sale/<sale_id>", methods = ["PUT"])
def complete_sale(sale_id):
    
    sale_to_complete = db.session.query(SaleTable).filter(SaleTable.sale_id == sale_id, SaleTable.completed == False).first()
    if not sale_to_complete:
        return jsonify ({"error": f"Venta de id {sale_id} no encontrada, verifique que exista y que no ha sido completada anteriormente"}), 404
    
    try:
        sale_to_complete.completed = True
        db.session.commit()
        db.session.refresh(sale_to_complete)
        return jsonify ({"message": "Venta completada correctamente",
                         "venta": {
                             "sale_id": sale_to_complete.sale_id,
                             "created_at": sale_to_complete.created_at,
                             "completed": sale_to_complete.completed
                         }})
        
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        
        

        



