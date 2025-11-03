# ---------------------------------------------
# --- Team Leader Authentication Blueprint ---
# ---------------------------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from db import get_db_connection

teamLeader_authenticate_bp = Blueprint("teamLeader_authenticate_bp", __name__)

# ---------------------------------------------
# --- Team Leader Signup ---
# ---------------------------------------------
@teamLeader_authenticate_bp.route("/teamLeader-signup", methods=["GET", "POST"])
def teamLeader_signup():
    """Handles team leader registration."""
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
            # Create leader with INACTIVE status (awaiting admin activation)
            cur.execute("""
                INSERT INTO users (username, email, password, name, surname, role, status)
                VALUES (%s, %s, %s, %s, %s, 'TEAM_LEADER', 'INACTIVE')
                RETURNING user_id, email;
            """, (username, email, password, name, surname))

            new_leader = cur.fetchone()
            conn.commit()

            session["teamLeader_id"] = new_leader["user_id"]
            session["teamLeader_email"] = new_leader["email"]
            flash(f"✅ Team Leader account created successfully for {new_leader['email']}! Awaiting admin activation.", "success")
            return redirect(url_for("teamLeader_authenticate_bp.teamLeader_login"))

        except Exception as e:
            conn.rollback()
            flash(f"❌ Error creating Team Leader: {e}", "error")
            return redirect(url_for("teamLeader_authenticate_bp.teamLeader_signup"))
        finally:
            cur.close()
            conn.close()

    return render_template("teamLeader_signup.html")


# ---------------------------------------------
# --- Team Leader Login ---
# ---------------------------------------------
@teamLeader_authenticate_bp.route("/teamLeader-login", methods=["GET", "POST"])
def teamLeader_login():
    """Handles team leader login."""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        if isinstance(conn, str):
            return f"❌ Database connection failed: {conn}"

        cur = conn.cursor(cursor_factory=RealDictCursor)
        try:
            cur.execute("""
                SELECT user_id, username, email, password, status
                FROM users
                WHERE email = %s AND role = 'TEAM_LEADER';
            """, (email,))
            leader = cur.fetchone()

            if not leader:
                flash("❌ No Team Leader account found with that email.", "error")
                return redirect(url_for("teamLeader_authenticate_bp.teamLeader_login"))

            if leader["password"] != password:
                flash("❌ Incorrect password.", "error")
                return redirect(url_for("teamLeader_authenticate_bp.teamLeader_login"))

            if leader["status"] != "ACTIVE":
                flash("⚠️ Account not active yet. Please wait for admin approval.", "warning")
                return redirect(url_for("teamLeader_authenticate_bp.teamLeader_login"))

            # ✅ Login successful
            session["teamLeader_id"] = leader["user_id"]
            session["teamLeader_email"] = leader["email"]
            session["teamLeader_username"] = leader["username"]

            flash("✅ Team Leader login successful!", "success")
            return redirect("/teamLeader-mainpage")

        except Exception as e:
            flash(f"❌ Error during login: {e}", "error")
            return redirect(url_for("teamLeader_authenticate_bp.teamLeader_login"))
        finally:
            cur.close()
            conn.close()

    return render_template("teamLeader_login.html")


# ---------------------------------------------
# --- Team Leader Logout ---
# ---------------------------------------------
@teamLeader_authenticate_bp.route("/teamLeader-logout")
def logout():
    """Logs out the team leader and clears the session."""
    session.clear()
    flash("✅ You have been logged out.", "success")
    return redirect("/")
