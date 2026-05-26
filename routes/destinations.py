from flask import Blueprint, jsonify, request, render_template
from models import Destination
from extensions import db

bp = Blueprint("destinations", __name__)


def _validate(data, partial=False):
    errors = {}

    for field in ("destination", "country"):
        if partial and field not in data:
            continue
        v = data.get(field, "")
        if not isinstance(v, str) or not v.strip():
            errors[field] = "must be a non-empty string"

    if not partial or "rating" in data:
        r = data.get("rating")
        if r is None and not partial:
            errors["rating"] = "required"
        elif r is not None:
            try:
                if not 0 <= float(r) <= 5:
                    errors["rating"] = "must be between 0 and 5"
            except (TypeError, ValueError):
                errors["rating"] = "must be a number"

    return errors


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/destinations", methods=["GET"])
def get_destinations():
    return jsonify([d.to_dict() for d in Destination.query.order_by(Destination.id).all()])


@bp.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    return jsonify(db.get_or_404(Destination, destination_id).to_dict())


@bp.route("/destinations", methods=["POST"])
def create_destination():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "expected JSON"}), 400

    errors = _validate(data)
    if errors:
        return jsonify({"error": "validation failed", "details": errors}), 422

    d = Destination(
        destination=data["destination"].strip(),
        country=data["country"].strip(),
        rating=float(data["rating"]),
    )
    db.session.add(d)
    db.session.commit()
    return jsonify(d.to_dict()), 201


@bp.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    d = db.get_or_404(Destination, destination_id)
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "expected JSON"}), 400

    errors = _validate(data, partial=True)
    if errors:
        return jsonify({"error": "validation failed", "details": errors}), 422

    if "destination" in data:
        d.destination = data["destination"].strip()
    if "country" in data:
        d.country = data["country"].strip()
    if "rating" in data:
        d.rating = float(data["rating"])

    db.session.commit()
    return jsonify(d.to_dict())


@bp.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    d = db.get_or_404(Destination, destination_id)
    db.session.delete(d)
    db.session.commit()
    return "", 204
