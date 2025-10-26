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
            # Insert the new team leader
            cur.execute("""
                INSERT INTO users (username, email, password, name, surname, role, status)
                VALUES (%s, %s, %s, %s, %s, 'TEAM_LEADER', 'ACTIVE')
            """, (username, email, password, name, surname))
            conn.commit()

            # No fetchone() needed — just use the form email
            session["teamLeader_email"] = email
            flash(f"✅ Team Leader account created successfully for {email}!", "success")
            return redirect("/teamLeader-mainpage")

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
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM users 
            WHERE email = %s AND password = %s AND role = 'TEAM_LEADER'
        """, (email, password))
        leader = cur.fetchone()

        cur.close()
        conn.close()

        if leader:
            session["teamLeader_id"] = leader[0]
            session["teamLeader_email"] = email
            flash("Team Leader login successful!", "success")
            return redirect("/teamLeader-mainpage")
        else:
            flash("Invalid email or password.", "danger")

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
