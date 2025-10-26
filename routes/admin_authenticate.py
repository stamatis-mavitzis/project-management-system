# ---------------------------------------------
# --- Admin Authentication Blueprint ---
# ---------------------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, session # type: ignore
from psycopg2.extras import RealDictCursor # type: ignore
from db import get_db_connection

admin_authenticate_bp = Blueprint("admin_authenticate_bp", __name__)

# ---------------------------------------------
# --- Admin Signup ---
# ---------------------------------------------
@admin_authenticate_bp.route("/admin-signup", methods=["GET", "POST"])
def admin_signup():
    """Handles admin registration."""
    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        if isinstance(conn, str):
            return f"❌ Database connection failed: {conn}"

        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                INSERT INTO users (username, email, password, name, surname, role, status)
                VALUES (%s, %s, %s, %s, %s, 'ADMIN', 'ACTIVE')
            """, (username, email, password, name, surname))
            conn.commit()
            flash("✅ Admin created successfully!", "success")
            return redirect(url_for("admin_authenticate_bp.admin_login"))
        except Exception as e:
            conn.rollback()
            flash(f"❌ Error creating admin: {e}", "error")
            return redirect(url_for("admin_authenticate_bp.admin_signup"))
        finally:
            cur.close()
            conn.close()

    return render_template("admin_signup.html")


# ---------------------------------------------
# --- Admin Login ---
# ---------------------------------------------
@admin_authenticate_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM users 
            WHERE email = %s AND password = %s AND role = 'ADMIN'
        """, (email, password))
        admin = cur.fetchone()

        cur.close()
        conn.close()

        if admin:
            session["admin_id"] = admin[0]
            session["admin_email"] = email  # Add this line
            flash("Admin login successful!", "success")
            return redirect("/admin-mainpage")
        else:
            flash("Invalid email or password.", "danger")

    return render_template("admin_login.html")



# ---------------------------------------------
# --- Admin Logout ---
# ---------------------------------------------
@admin_authenticate_bp.route("/logout")
def logout():
    """Logs out the admin and clears the session."""
    session.clear()
    flash("✅ You have been logged out.", "success")
    return redirect("/")
