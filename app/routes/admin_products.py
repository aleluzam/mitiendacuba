from flask import Blueprint, jsonify
from database import db
from models.products_models import ProductTable
from models.subproducts_models import SubproductTable
from security import login_required

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.route('/', methods=["GET"])
def get_products():
    products = db.session.query(ProductTable).all()  
    return jsonify([p.to_dict() for p in products])


@products_bp.route("/subproducts", methods=["GET"])
def all_subproducts():
    subproducts = db.session.query(SubproductTable).all()
    return jsonify ([p.to_dict() for p in subproducts])





