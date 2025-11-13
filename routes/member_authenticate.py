# ---------------------------------------------
# --- Member Authentication Blueprint ---
# ---------------------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from db import get_db_connection

member_authenticate_bp = Blueprint("member_authenticate_bp", __name__)

# ---------------------------------------------
# --- Member Signup ---
# ---------------------------------------------
@member_authenticate_bp.route("/member-signup", methods=["GET", "POST"])
def member_signup():
    """Handles member registration."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        surname = request.form.get("surname")

        conn = get_db_connection()
        if isinstance(conn, str):
            return f"❌ Database connection failed: {conn}"

        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Insert new member and return their user_id
            cur.execute("""
                INSERT INTO users (username, email, password, name, surname, role, status)
                VALUES (%s, %s, %s, %s, %s, 'MEMBER', 'INACTIVE')
                RETURNING user_id, email;
            """, (username, email, password, name, surname))

            new_user = cur.fetchone()
            conn.commit()

            session["member_id"] = new_user["user_id"]
            session["member_email"] = new_user["email"]
            flash(f"✅ Member account created successfully for {new_user['email']}! Awaiting admin activation.", "success")
            return redirect(url_for("member_authenticate_bp.member_login"))

        except Exception as e:
            conn.rollback()
            flash(f"❌ Error creating Member: {e}", "error")
            return redirect(url_for("member_authenticate_bp.member_login"))
        finally:
            cur.close()
            conn.close()

    return render_template("member_signup.html")


# ---------------------------------------------
# --- Member Login ---
# ---------------------------------------------
@member_authenticate_bp.route("/member-login", methods=["GET", "POST"])
def member_login():
    """Handles member login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        if isinstance(conn, str):
            return f"❌ Database connection failed: {conn}"

        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            # Select user_id instead of id
            cur.execute("""
                SELECT user_id, username, email, password, status
                FROM users
                WHERE email = %s AND role = 'MEMBER';
            """, (email,))
            member = cur.fetchone()

            if not member:
                flash("❌ No member account found with that email.", "error")
                return redirect(url_for("member_authenticate_bp.member_login"))

            if member["password"] != password:
                flash("❌ Incorrect password.", "error")
                return redirect(url_for("member_authenticate_bp.member_login"))

            if member["status"] != "ACTIVE":
                flash("⚠️ Account not active yet. Please wait for admin approval.", "warning")
                return redirect(url_for("member_authenticate_bp.member_login"))

            # ✅ Login successful
            session["member_id"] = member["user_id"]
            session["member_email"] = member["email"]
            session["member_username"] = member["username"]

            flash("✅ Member login successful!", "success")
            return redirect(url_for("member_mainpage_bp.member_mainpage"))

        except Exception as e:
            flash(f"❌ Error during login: {e}", "error")
            return redirect(url_for("member_authenticate_bp.member_login"))
        finally:
            cur.close()
            conn.close()

    return render_template("member_login.html")


# ---------------------------------------------
# --- Member Logout ---
# ---------------------------------------------
@member_authenticate_bp.route("/member-logout")
def logout():
    """Logs out the member and clears the session."""
    session.clear()
    flash("✅ You have been logged out.", "success")
    return redirect("/")
