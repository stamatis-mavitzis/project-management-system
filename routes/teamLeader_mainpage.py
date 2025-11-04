from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from db import get_db_connection

teamLeader_mainpage_bp = Blueprint("teamLeader_mainpage_bp", __name__)

# ---------------------------------------------
# --- Team Leader Dashboard / Main Page ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-mainpage")
def teamLeader_mainpage():
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    leader_email = session["teamLeader_email"]

    # Πάρε username και email από τη βάση
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, email FROM users WHERE email = %s;", (leader_email,))
    leader = cur.fetchone()
    cur.close()
    conn.close()

    if not leader:
        flash("Team Leader not found in database.", "error")
        return redirect("/teamLeader-login")

    # Στείλε τα δεδομένα στο template
    return render_template("teamLeader_mainpage.html", leader=leader)


# ---------------------------------------------
# --- Manage Teams (Team Leader) ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-manageTeams")
def teamLeader_manage_teams():
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    leader_email = session["teamLeader_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get leader's user_id
    cur.execute("SELECT user_id FROM users WHERE email = %s;", (leader_email,))
    user_row = cur.fetchone()
    if not user_row:
        flash("User not found.", "error")
        return redirect("/teamLeader-login")

    user_id = user_row["user_id"]

    # Get all teams where the leader is either the leader OR a member
    cur.execute("""
        SELECT 
            t.team_id,
            t.name,
            t.description,
            COUNT(m.user_id) AS member_count,
            CASE WHEN t.leader_id = %s THEN TRUE ELSE FALSE END AS is_leader
        FROM teams t
        LEFT JOIN team_members m ON t.team_id = m.team_id
        WHERE t.team_id IN (
            SELECT team_id FROM team_members WHERE user_id = %s
            UNION
            SELECT team_id FROM teams WHERE leader_id = %s
        )
        GROUP BY t.team_id, t.name, t.description, t.leader_id
        ORDER BY t.name;
    """, (user_id, user_id, user_id))

    teams = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("teamLeader_manageTeams.html", teams=teams)


# ---------------------------------------------
# --- Manage Single Team ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-manageTeam/<int:team_id>")
def teamLeader_manage_team(team_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get team details (including team_id)
    cur.execute("""
        SELECT t.team_id, t.name, t.description, u.username AS leader_name
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.user_id
        WHERE t.team_id = %s;
    """, (team_id,))
    team = cur.fetchone()

    # Get members
    cur.execute("""
        SELECT u.username, u.email, u.role, u.status
        FROM team_members tm
        JOIN users u ON tm.user_id = u.user_id
        WHERE tm.team_id = %s;
    """, (team_id,))
    members = cur.fetchall()

    # Get tasks for this team (including priority)
    cur.execute("""
        SELECT 
            t.task_id,
            t.title,
            t.description,
            t.status,
            t.priority,
            t.due_date,
            u.username AS assigned_to
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.user_id
        WHERE t.team_id = %s
        ORDER BY t.created_at DESC;
    """, (team_id,))
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "teamLeader_teamDetails.html",
        team=team,
        members=members,
        tasks=tasks,
        team_id=team_id
    )


# ---------------------------------------------
# --- Add Member to Team ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-addMember/<int:team_id>", methods=["POST"])
def add_member(team_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    member_email = request.form.get("member_email")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT user_id FROM users WHERE email = %s;", (member_email,))
    user = cur.fetchone()
    if not user:
        flash("User not found.", "error")
    else:
        cur.execute("""
            INSERT INTO team_members (team_id, user_id)
            VALUES (%s, %s)
            ON CONFLICT DO NOTHING;
        """, (team_id, user["user_id"]))
        conn.commit()
        flash("Member added successfully!", "success")

    cur.close()
    conn.close()
    return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_team", team_id=team_id))


# ---------------------------------------------
# --- Remove Member from Team ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-removeMember/<int:team_id>", methods=["POST"])
def remove_member(team_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    email = request.form.get("email")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT user_id FROM users WHERE email = %s;", (email,))
    user = cur.fetchone()
    if user:
        cur.execute("DELETE FROM team_members WHERE team_id = %s AND user_id = %s;", (team_id, user["user_id"]))
        conn.commit()
        flash("Member removed successfully!", "success")
    else:
        flash("User not found.", "error")

    cur.close()
    conn.close()
    return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_team", team_id=team_id))


# ---------------------------------------------
# --- Create Task for Team ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-createTask/<int:team_id>", methods=["POST"])
def create_task(team_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    title = request.form.get("title")
    description = request.form.get("description")
    assigned_email = request.form.get("assigned_to")
    due_date = request.form.get("due_date")
    priority = request.form.get("priority").upper()  # ✅ Fix here

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT user_id FROM users WHERE email = %s;", (session["teamLeader_email"],))
    leader = cur.fetchone()
    if not leader:
        flash("Leader not found.", "error")
        return redirect("/teamLeader-login")

    cur.execute("SELECT user_id FROM users WHERE email = %s;", (assigned_email,))
    assigned = cur.fetchone()
    if not assigned:
        flash("Assigned user not found.", "error")
        return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_team", team_id=team_id))

    cur.execute("""
        INSERT INTO tasks (title, description, created_by, assigned_to, team_id, status, priority, due_date, created_at)
        VALUES (%s, %s, %s, %s, %s, 'TODO', %s, %s, NOW());
    """, (title, description, leader["user_id"], assigned["user_id"], team_id, priority, due_date))
    conn.commit()

    cur.close()
    conn.close()

    flash("Task created successfully!", "success")
    return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_team", team_id=team_id))


# ---------------------------------------------
# --- View Task Details (with Comments) ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-viewTask/<int:task_id>")
def view_task(task_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # -------------------------------
        # 🔹 Λήψη στοιχείων του task
        # -------------------------------
        cur.execute("""
            SELECT 
                t.task_id,
                t.title,
                t.description,
                t.status,
                t.priority,
                t.due_date,
                t.team_id,  -- ✅ Add this line
                cu.username AS created_by_username,
                au.username AS assigned_to_username
            FROM tasks t
            JOIN users cu ON t.created_by = cu.user_id
            JOIN users au ON t.assigned_to = au.user_id
            WHERE t.task_id = %s;
        """, (task_id,))
        task = cur.fetchone()

        if not task:
            flash("Task not found.", "error")
            return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_teams"))

        # -------------------------------
        # 💬 Λήψη σχολίων του task
        # -------------------------------
        cur.execute("""
            SELECT 
                c.content, 
                c.created_at, 
                u.username
            FROM comments c
            JOIN users u ON c.author_id = u.user_id
            WHERE c.task_id = %s
            ORDER BY c.created_at DESC;
        """, (task_id,))
        comments = cur.fetchall()

    except Exception as e:
        conn.rollback()
        flash(f"Error loading task: {e}", "error")
        comments = []
        task = None

    finally:
        cur.close()
        conn.close()

    if not task:
        return redirect(url_for("teamLeader_mainpage_bp.teamLeader_manage_teams"))

    # ✅ Pass team_id to template
    return render_template("teamLeader_viewTask.html", task=task, comments=comments, team_id=task["team_id"])




# ---------------------------------------------
# --- Edit Task ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-editTask/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        status = request.form.get("status")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority").upper()

        

        cur.execute("""
            UPDATE tasks
            SET title = %s, description = %s, status = %s, due_date = %s, priority = %s
            WHERE task_id = %s;
        """, (title, description, status, due_date, priority, task_id))
        conn.commit()

        flash("Task updated successfully!", "success")
        cur.close()
        conn.close()
        return redirect(url_for("teamLeader_mainpage_bp.view_task", task_id=task_id))

    cur.execute("SELECT * FROM tasks WHERE task_id = %s;", (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("teamLeader_editTask.html", task=task)


# ---------------------------------------------
# --- Delete Task ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-deleteTask/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE task_id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

    flash("Task deleted successfully!", "success")
    return redirect("/teamLeader-manageTeams")




# ---------------------------------------------
# --- Manage Tasks & Projects (with Team Names) ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-manageTasksProjects")
def teamLeader_manage_tasks_projects():
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    leader_email = session["teamLeader_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # -------------------------------
    # Get the user_id of the leader
    # -------------------------------
    cur.execute("SELECT user_id FROM users WHERE email = %s", (leader_email,))
    leader_row = cur.fetchone()
    if not leader_row:
        flash("Leader not found.", "error")
        cur.close()
        conn.close()
        return redirect("/teamLeader-mainpage")

    leader_id = leader_row["user_id"]

    # -------------------------------
    # Get all teams of this leader
    # -------------------------------
    cur.execute("""
        SELECT team_id, name AS team_name, description
        FROM teams
        WHERE leader_id = %s
    """, (leader_id,))
    teams = cur.fetchall()

    # -------------------------------
    # Get all tasks of the leader’s teams
    # Include assigned username and team name
    # -------------------------------
    cur.execute("""
        SELECT 
            t.task_id, 
            t.title, 
            t.description, 
            t.status, 
            t.due_date, 
            t.priority, 
            COALESCE(u.username, 'Unassigned') AS assigned_username,
            tm.name AS team_name
        FROM tasks t
        LEFT JOIN users u ON t.assigned_to = u.user_id
        LEFT JOIN teams tm ON t.team_id = tm.team_id
        WHERE tm.leader_id = %s
        ORDER BY tm.name ASC, t.due_date ASC;
    """, (leader_id,))
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "teamLeader_manageTasksProjects.html",
        teams=teams,
        tasks=tasks,
        email=leader_email
    )



# ---------------------------------------------
# --- Add Comment to Task ---
# ---------------------------------------------
@teamLeader_mainpage_bp.route("/teamLeader-addComment/<int:task_id>", methods=["POST"])
def add_comment(task_id):
    if "teamLeader_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/teamLeader-login")

    content = request.form.get("content")

    if not content:
        flash("Comment cannot be empty.", "error")
        return redirect(url_for("teamLeader_mainpage_bp.view_task", task_id=task_id))

    leader_email = session["teamLeader_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get the author_id (user_id) of the currently logged-in team leader
    cur.execute("SELECT user_id FROM users WHERE email = %s", (leader_email,))
    author_row = cur.fetchone()

    if not author_row:
        flash("Error: User not found.", "error")
        cur.close()
        conn.close()
        return redirect(url_for("teamLeader_mainpage_bp.view_task", task_id=task_id))

    author_id = author_row["user_id"]

    # Insert the comment using the correct column name 'author_id'
    cur.execute("""
        INSERT INTO comments (task_id, author_id, content, created_at)
        VALUES (%s, %s, %s, NOW())
    """, (task_id, author_id, content))

    conn.commit()
    cur.close()
    conn.close()

    flash("✅ Comment added successfully!", "success")
    return redirect(url_for("teamLeader_mainpage_bp.view_task", task_id=task_id))
