from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models import QAPair, User  # Assuming these are exported from app/models.py, and the db is initialized there
from app import db


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Add new FAQ
@admin_bp.route("/add", methods=["POST"])
def admin_add():
    data = request.get_json(silent=True)
    if not data or "question" not in data or "answer" not in data:
        return jsonify({"error": "Please provide both 'question' and 'answer'."}), 400

    if QAPair.query.filter_by(question=data["question"]).first():
        return jsonify({"error": "This question already exists."}), 400

    new_qa = QAPair(
        question=data["question"],
        answer=data["answer"],
        is_enabled=data.get("is_enabled", True)
    )
    db.session.add(new_qa)
    db.session.commit()
    return jsonify({"message": "Q&A pair added successfully."}), 201

# Edit existing FAQ
@admin_bp.route("/edit/<int:qa_id>", methods=["PUT"])
def admin_edit(qa_id):
    qa = QAPair.query.get_or_404(qa_id)
    data = request.get_json(silent=True)

    qa.question = data.get("question", qa.question)
    qa.answer = data.get("answer", qa.answer)
    if "is_enabled" in data:
        qa.is_enabled = data["is_enabled"]

    db.session.commit()
    return jsonify({"message": "Q&A pair updated successfully."})

# Delete FAQ
@admin_bp.route("/delete/<int:qa_id>", methods=["DELETE"])
def admin_delete(qa_id):
    qa = QAPair.query.get_or_404(qa_id)
    db.session.delete(qa)
    db.session.commit()
    return jsonify({"message": "Q&A pair deleted successfully."})

# Toggle enable/disable FAQ
@admin_bp.route("/toggle/<int:qa_id>", methods=["POST"])
def admin_toggle(qa_id):
    qa = QAPair.query.get_or_404(qa_id)
    qa.is_enabled = not qa.is_enabled
    db.session.commit()
    return jsonify({"message": f"Q&A pair {'enabled' if qa.is_enabled else 'disabled'} successfully."})

# Optional: Get all FAQs (including disabled)
@admin_bp.route("/list", methods=["GET"])
def admin_list():
    faqs = QAPair.query.all()
    return jsonify([
        {
            "id": faq.id,
            "question": faq.question,
            "answer": faq.answer,
            "is_enabled": faq.is_enabled
        } for faq in faqs
    ])


