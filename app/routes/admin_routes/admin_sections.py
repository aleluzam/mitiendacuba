from flask import jsonify, request, Blueprint
from app.database import db
from app.models.sections_models import SectionCreate, SectionPublic, SectionTable, SectionUpdate
from pydantic import ValidationError


admin_sections_bp = Blueprint("sections", __name__, url_prefix="/admin")



# CREAR SECCION
@admin_sections_bp.route("/section/create", methods = ["POST"])
def create_section():
    try:
        data = SectionCreate.model_validate(request.get_json())
        
        new_section = SectionTable(
            name = data.name,
            description = data.description,
            img = data.img
        )
        db.session.add(new_section)
        db.session.commit()
        db.session.refresh(new_section)
        
        return jsonify ({"message": "Seccion creada satisfactoriamente",
                         "section": {
                             "name": new_section.name,
                             "description": new_section.description
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
        
 
 
# EDITAR SECCION
@admin_sections_bp.route("/section/edit/<id>", methods = ["PUT"])
def edit_section(id):
    
    section_to_edit = db.session.query(SectionTable).filter(SectionTable.id == id).first()
    if not section_to_edit:
        return jsonify ({"error": f"La seccion de id {id} no existe"}), 404
    
    try:
        data = SectionUpdate.model_validate(request.get_json())  
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(section_to_edit, field, value)
        
        db.session.commit()
        db.session.refresh(section_to_edit)
        return jsonify ({"message": "Seccion editada correctamente",
                         "section": SectionPublic.model_validate(section_to_edit).model_dump()})
    
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
        
        
            
# VER TODAS LAS SECCIONES
@admin_sections_bp.route("/section/all", methods = ["GET"])
def get_all_sections():
    
    all_sections = db.session.query(SectionTable).all()
    if not all_sections:
        return jsonify ({"message": "No hay secciones actualmente"})
    
    try:
        
        return jsonify ([SectionPublic.model_validate(section).model_dump() for section in all_sections])

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
        
        
