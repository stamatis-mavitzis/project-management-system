# ---------------------------------------------
# --- Admin Authentication Blueprint ---
# ---------------------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
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
            return f"Database connection failed: {conn}"

        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Create admin with INACTIVE status (awaiting activation)
            cur.execute("""
                INSERT INTO users (username, email, password, name, surname, role, status)
                VALUES (%s, %s, %s, %s, %s, 'ADMIN', 'INACTIVE')
                RETURNING email;
            """, (username, email, password, name, surname))
            new_admin = cur.fetchone()
            conn.commit()

            flash(f"Admin account created successfully for {new_admin['email']}! Awaiting admin activation.", "success")
            return redirect(url_for("admin_authenticate_bp.admin_login"))
        except Exception as e:
            conn.rollback()
            flash(f"Error creating admin: {e}", "error")
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
    """Handles admin login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT user_id, username, email, password, status
                FROM users
                WHERE email = %s AND role = 'ADMIN';
            """, (email,))
            admin = cur.fetchone()

            if not admin:
                flash("No admin account found with that email.", "error")
                return redirect(url_for("admin_authenticate_bp.admin_login"))

            if admin["password"] != password:
                flash("Incorrect password.", "error")
                return redirect(url_for("admin_authenticate_bp.admin_login"))

            if admin["status"] != "ACTIVE":
                flash("⚠️ Account not active yet. Please wait for admin approval.", "warning")
                return redirect(url_for("admin_authenticate_bp.admin_login"))

            # ✅ Login successful
            session["admin_id"] = admin["user_id"]
            session["admin_email"] = admin["email"]
            session["admin_username"] = admin["username"]

            flash("✅ Admin login successful!", "success")
            return redirect("/admin-mainpage")

        except Exception as e:
            flash(f"Error during login: {e}", "error")
            return redirect(url_for("admin_authenticate_bp.admin_login"))
        finally:
            cur.close()
            conn.close()

    return render_template("admin_login.html")


# ---------------------------------------------
# --- Admin Logout ---
# ---------------------------------------------
@admin_authenticate_bp.route("/logout")
def logout():
    """Logs out the admin and clears the session."""
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/")
