from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from db import get_db_connection
from config import ALLOWED_EXTENSIONS
from utils.file_utils import allowed_file

admin_mainpage_bp = Blueprint("admin_mainpage_bp", __name__)

# ---------------------------------------------
# --- Admin Dashboard / Main Page ---
# ---------------------------------------------
@admin_mainpage_bp.route("/admin-mainpage")
def admin_mainpage():
    if "admin_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/admin-login")

    admin_email = session["admin_email"]

    # Fetch admin username from DB
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, email FROM users WHERE email = %s;", (admin_email,))
    admin = cur.fetchone()
    conn.close()

    if not admin:
        flash("Admin not found in database.", "error")
        return redirect("/admin-login")

    return render_template("admin_mainpage.html", admin=admin)


# ---------------------------------------------
# --- Manage Users ---
# ---------------------------------------------
@admin_mainpage_bp.route("/admin-manageUsers")
def admin_manage_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, email, role, status FROM users ORDER BY username;")
    users = cur.fetchall()
    conn.close()
    return render_template("admin_manageUsers.html", users=users)


# ---------------------------------------------
# --- Manage Teams ---
# ---------------------------------------------
@admin_mainpage_bp.route("/admin-manageTeams", methods=["GET", "POST"])
def admin_manage_teams():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == "POST":
        team_name = request.form.get("team_name")
        description = request.form.get("description")
        leader_username = request.form.get("leader_username")

        if not all([team_name, description, leader_username]):
            flash("⚠️ Please fill in all fields.", "error")
            return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

        cur.execute(
            "SELECT user_id FROM users WHERE username = %s AND role = 'TEAM_LEADER';",
            (leader_username,),
        )
        leader = cur.fetchone()

        if not leader:
            flash("❌ Leader not found or not a TEAM_LEADER.", "error")
            conn.close()
            return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

        leader_id = leader["user_id"]

        cur.execute("""
            INSERT INTO teams (name, description, leader_id, created_at)
            VALUES (%s, %s, %s, NOW());
        """, (team_name, description, leader_id))
        conn.commit()
        flash("✅ Team created successfully!", "success")
        return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

    cur.execute("""
    SELECT 
        t.team_id,
        t.name,
        t.description,
        u.username AS leader,
        COALESCE(STRING_AGG(m.username, ', '), 'No members') AS members
    FROM teams t
    LEFT JOIN users u ON t.leader_id = u.user_id
    LEFT JOIN team_members tm ON t.team_id = tm.team_id
    LEFT JOIN users m ON tm.user_id = m.user_id
    GROUP BY t.team_id, t.name, t.description, u.username, t.created_at
    ORDER BY t.created_at DESC;
    """)
    teams = cur.fetchall()

    conn.close()
    return render_template("admin_manageTeams.html", teams=teams)


# ---------------------------------------------
# --- Show All Tasks & Projects ---
# ---------------------------------------------
@admin_mainpage_bp.route("/admin-show_tasks_and_projects")
def admin_show_tasks_and_projects():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM teams ORDER BY created_at DESC;")
    projects = cur.fetchall()
    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("admin_show_tasks_and_projects.html", projects=projects, tasks=tasks)


# ---------------------------------------------
# --- Activate / Deactivate / Change Role ---
# ---------------------------------------------
@admin_mainpage_bp.route("/activate_user/<string:username>", methods=["POST"])
def activate_user(username):
    """Activate a user account."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("UPDATE users SET status = 'ACTIVE' WHERE username = %s;", (username,))
        conn.commit()
        return jsonify({"message": f"✅ User {username} activated successfully!"}), 200
    except Exception as e:
        conn.rollback()
        print("❌ ERROR activating user:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@admin_mainpage_bp.route("/deactivate_user/<string:username>", methods=["POST"])
def deactivate_user(username):
    """Deactivate a user account."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("UPDATE users SET status = 'INACTIVE' WHERE username = %s;", (username,))
        conn.commit()
        return jsonify({"message": f"⚠️ User {username} deactivated."}), 200
    except Exception as e:
        conn.rollback()
        print("❌ ERROR deactivating user:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@admin_mainpage_bp.route("/change_role/<string:username>", methods=["POST"])
def change_role(username):
    """Change the user's role (ADMIN / TEAM_LEADER / MEMBER)."""
    new_role = request.json.get("role")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("UPDATE users SET role = %s WHERE username = %s;", (new_role, username))
        conn.commit()
        return jsonify({"message": f"✅ Role for {username} changed to {new_role}"}), 200
    except Exception as e:
        conn.rollback()
        print("❌ ERROR changing role:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# --- View Team Details ---
@admin_mainpage_bp.route("/admin-viewTeam/<int:team_id>")
def admin_view_team(team_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT 
            t.team_id, 
            t.name, 
            t.description, 
            u.username AS leader
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.user_id
        WHERE t.team_id = %s;
    """, (team_id,))
    team = cur.fetchone()

    cur.execute("""
        SELECT u.username, u.email, u.role
        FROM team_members tm
        JOIN users u ON tm.user_id = u.user_id
        WHERE tm.team_id = %s;
    """, (team_id,))
    members = cur.fetchall()

    conn.close()
    return render_template("admin_viewTeam.html", team=team, members=members)


# --- Delete Team ---
@admin_mainpage_bp.route("/admin-deleteTeam/<int:team_id>", methods=["POST"])
def admin_delete_team(team_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Delete team members first to maintain integrity
        cur.execute("DELETE FROM team_members WHERE team_id = %s;", (team_id,))
        cur.execute("DELETE FROM teams WHERE team_id = %s;", (team_id,))
        conn.commit()
        return jsonify({"message": "✅ Team deleted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        print("❌ ERROR deleting team:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()