from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.utils.chatbot import get_reply

from flask_login import login_user, logout_user, login_required
from app.models import QAPair, User  # Import User so that login functionality works

main_bp = Blueprint("main", __name__)

# Home page (chatbot)
@main_bp.route("/")
def home():
    return render_template("index.html")  # Ensure templates/index.html exists

# Chatbot interaction endpoint
@main_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Please provide a 'message' key in the JSON data."}), 400

    user_input = data["message"]
    # Get a reply using the hybrid model (FAQ retrieval + fallback ChatBot)
    reply = get_reply(user_input)
    return jsonify({"reply": reply})

# Chatbox HTML page
@main_bp.route("/chatbox")
def chatbot():
    return render_template("chat_widget.html")  # Ensure templates/chat_widget.html exists

# Admin Panel HTML page
@main_bp.route("/admin-panel")
@login_required
def admin_panel():
    return render_template("admin_panel.html")  # Ensure templates/admin_panel.html exists

# Admin Login
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            # Redirect to admin panel instead of dashboard
            return redirect(url_for('main.admin_panel'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main.login'))
    return render_template('admin/login.html')


# Admin Dashboard (protected route)
@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

# Admin Logout
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
