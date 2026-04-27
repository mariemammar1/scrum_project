from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Service, Employee, Supplier

secondary_bp = Blueprint("secondary", __name__)

# SERVICES
@secondary_bp.route("/services", methods=["POST"])
@jwt_required()
def create_service():
    s = Service(**request.json)
    db.session.add(s)
    db.session.commit()
    return {"message": "Service created"}


@secondary_bp.route("/services/<int:id>", methods=["PUT"])
@jwt_required()
def edit_service(id):
    s = Service.query.get_or_404(id)
    data = request.json
    s.name = data["name"]
    s.price = data["price"]
    db.session.commit()
    return {"message": "Service updated"}


@secondary_bp.route("/services/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_service(id):
    s = Service.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return {"message": "Service deleted"}


# EMPLOYEES
@secondary_bp.route("/employees", methods=["POST"])
@jwt_required()
def create_employee():
    e = Employee(**request.json)
    db.session.add(e)
    db.session.commit()
    return {"message": "Employee created"}


@secondary_bp.route("/employees/<int:id>", methods=["PUT"])
@jwt_required()
def edit_employee(id):
    e = Employee.query.get_or_404(id)
    data = request.json
    e.name = data["name"]
    e.role = data["role"]
    e.salary = data["salary"]
    db.session.commit()
    return {"message": "Employee updated"}


@secondary_bp.route("/employees/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_employee(id):
    e = Employee.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return {"message": "Employee deleted"}


# SUPPLIERS
@secondary_bp.route("/suppliers", methods=["POST"])
@jwt_required()
def create_supplier():
    s = Supplier(**request.json)
    db.session.add(s)
    db.session.commit()
    return {"message": "Supplier created"}


@secondary_bp.route("/suppliers/<int:id>", methods=["PUT"])
@jwt_required()
def edit_supplier(id):
    s = Supplier.query.get_or_404(id)
    data = request.json
    s.name = data["name"]
    s.contact = data["contact"]
    db.session.commit()
    return {"message": "Supplier updated"}


@secondary_bp.route("/suppliers/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(id):
    s = Supplier.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return {"message": "Supplier deleted"}


# FILTER
@secondary_bp.route("/search", methods=["GET"])
@jwt_required()
def search():
    name = request.args.get("name", "")

    return {
        "services": [s.name for s in Service.query.filter(Service.name.contains(name)).all()],
        "employees": [e.name for e in Employee.query.filter(Employee.name.contains(name)).all()],
        "suppliers": [s.name for s in Supplier.query.filter(Supplier.name.contains(name)).all()],
    }
@secondary_bp.route("/services", methods=["GET"])
def list_services():
    return [{"id": s.id, "name": s.name, "price": s.price} for s in Service.query.all()]


@secondary_bp.route("/employees", methods=["GET"])
def list_employees():
    return [{"id": e.id, "name": e.name, "role": e.role} for e in Employee.query.all()]


@secondary_bp.route("/suppliers", methods=["GET"])
def list_suppliers():
    return [{"id": s.id, "name": s.name, "contact": s.contact} for s in Supplier.query.all()]