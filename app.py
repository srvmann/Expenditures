import re
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = 'spendly-secret-key-change-in-production'


def csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']


# Make csrf_token available in templates
app.jinja_env.globals['csrf_token'] = lambda: csrf_token()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # CSRF validation
        submitted_token = request.form.get("csrf_token", "")
        if submitted_token != session.get("csrf_token"):
            flash("Invalid form submission", "error")
            return render_template("register.html")

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        errors = []
        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Invalid email format")
        if not password:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be at least 8 characters")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html", name=name, email=email)

        # Check for duplicate email
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            flash("An account with this email already exists", "error")
            return render_template("register.html", name=name, email=email)

        # Insert new user
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # CSRF validation
        submitted_token = request.form.get("csrf_token", "")
        if submitted_token != session.get("csrf_token"):
            flash("Invalid form submission", "error")
            return render_template("login.html")

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        if not email or not password:
            flash("Email and password are required", "error")
            return render_template("login.html", email=email)

        # Check credentials
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, password_hash FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password", "error")
            return render_template("login.html", email=email)

        # Login successful - create session
        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    user_name = session.get("user_name", "User")
    session.clear()
    flash(f"Goodbye, {user_name}! You have been signed out.", "success")
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Hardcoded data for UI validation (Step 4 only)
    user_info = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2025"
    }

    summary_stats = {
        "total_spent": 454.98,
        "transaction_count": 8,
        "top_category": "Food"
    }

    transactions = [
        {"date": "2026-04-18", "description": "Gift for friend", "category": "Other", "amount": 50.00},
        {"date": "2026-04-15", "description": "Restaurant dinner", "category": "Food", "amount": 32.50},
        {"date": "2026-04-12", "description": "New headphones", "category": "Shopping", "amount": 89.00},
    ]

    category_breakdown = [
        {"name": "Food", "total": 78.49, "percentage": 17},
        {"name": "Shopping", "total": 89.00, "percentage": 20},
        {"name": "Bills", "total": 120.00, "percentage": 26},
    ]

    return render_template("profile.html",
                           user_info=user_info,
                           summary_stats=summary_stats,
                           transactions=transactions,
                           category_breakdown=category_breakdown)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
