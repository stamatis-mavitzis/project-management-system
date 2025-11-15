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
    """Displays all users with signup and activation (update) dates."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT 
            username,
            email,
            role,
            status,
            TO_CHAR(created_at, 'DD/MM/YY HH24:MI') AS signup_date,
            TO_CHAR(updated_at, 'DD/MM/YY HH24:MI') AS activated_date
        FROM users
        ORDER BY username;
    """)

    users = cur.fetchall()
    cur.close()
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
            flash("Please fill in all fields.", "error")
            return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

        cur.execute(
            "SELECT user_id FROM users WHERE username = %s AND role = 'TEAM_LEADER';",
            (leader_username,),
        )
        leader = cur.fetchone()

        if not leader:
            flash("Leader not found or not a TEAM_LEADER.", "error")
            conn.close()
            return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

        leader_id = leader["user_id"]

        cur.execute("""
            INSERT INTO teams (name, description, leader_id, created_at)
            VALUES (%s, %s, %s, NOW());
        """, (team_name, description, leader_id))
        conn.commit()
        flash("Team created successfully!", "success")
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
# --- Activate / Deactivate / Change Role ---
# ---------------------------------------------
@admin_mainpage_bp.route("/activate_user/<string:username>", methods=["POST"])
def activate_user(username):
    """Activate a user account and record activation timestamp."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            UPDATE users
            SET status = 'ACTIVE',
                updated_at = NOW()
            WHERE username = %s;
        """, (username,))
        conn.commit()
        return jsonify({"message": f"User {username} activated successfully!"}), 200
    except Exception as e:
        conn.rollback()
        print("ERROR activating user:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@admin_mainpage_bp.route("/deactivate_user/<string:username>", methods=["POST"])
def deactivate_user(username):
    """Deactivate any user account."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("UPDATE users SET status = 'INACTIVE' WHERE username = %s;", (username,))
        conn.commit()
        return jsonify({"message": f"User {username} deactivated."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------
# --- View Single Team Details ---
# ---------------------------------------------
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
        SELECT u.username, u.email, u.role, u.status
        FROM team_members tm
        JOIN users u ON tm.user_id = u.user_id
        WHERE tm.team_id = %s;
    """, (team_id,))
    members = cur.fetchall()

    cur.close()
    conn.close()

    if not team:
        flash("Team not found.", "error")
        return redirect(url_for("admin_mainpage_bp.admin_manage_teams"))

    return render_template("admin_viewTeam.html", team=team, members=members)


@admin_mainpage_bp.route("/admin-show_tasks_and_projects")
def admin_show_tasks_and_projects():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get all projects (teams)
    cur.execute("""
        SELECT 
            t.team_id,
            t.name AS team_name,
            t.description,
            t.created_at,
            u.username AS leader_name
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.user_id
        ORDER BY t.created_at DESC;
    """)
    projects = cur.fetchall()

    # Get all tasks including the leader who assigned them
    cur.execute("""
        SELECT 
            ta.task_id,
            ta.title,
            ta.description,
            ta.status,
            ta.priority,
            ta.due_date,
            ta.created_at,
            assignee.username AS assigned_to,
            leader.username AS assigned_by,
            tm.name AS team_name
        FROM tasks ta
        LEFT JOIN users assignee ON ta.assigned_to = assignee.user_id
        LEFT JOIN users leader ON ta.created_by = leader.user_id
        LEFT JOIN teams tm ON ta.team_id = tm.team_id
        ORDER BY ta.created_at DESC;
    """)
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "admin_show_tasks_and_projects.html",
        projects=projects,
        tasks=tasks
    )


