from flask import Blueprint, render_template, request, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from db import get_db_connection

from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import os

member_mainpage_bp = Blueprint("member_mainpage_bp", __name__)

# ---------------------------------------------
# Member Dashboard / Main Page ---
# ---------------------------------------------
@member_mainpage_bp.route("/member-mainpage")
def member_mainpage():
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    member_email = session["member_email"]

    # Fetch username and email from DB
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT username, email FROM users WHERE email = %s;", (member_email,))
    member = cur.fetchone()
    cur.close()
    conn.close()

    if not member:
        flash("Member not found in database.", "error")
        return redirect("/member-login")

    return render_template("member_mainpage.html", member=member)


# ---------------------------------------------
# Teams Included
# ---------------------------------------------
@member_mainpage_bp.route("/member-teamsIncluded")
def member_teams_included():
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    member_email = session["member_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get the member's user_id
    cur.execute("SELECT user_id, username FROM users WHERE email = %s;", (member_email,))
    member = cur.fetchone()
    if not member:
        flash("Member not found.", "error")
        conn.close()
        return redirect("/member-login")

    member_id = member["user_id"]

    # Get all teams where this member participates
    cur.execute("""
        SELECT 
            t.team_id,
            t.name AS team_name,
            t.description,
            u.username AS leader_name,
            COUNT(tm2.user_id) AS member_count
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.user_id
        LEFT JOIN team_members tm2 ON t.team_id = tm2.team_id
        WHERE t.team_id IN (
            SELECT team_id FROM team_members WHERE user_id = %s
        )
        GROUP BY t.team_id, t.name, t.description, u.username
        ORDER BY t.name;
    """, (member_id,))
    teams = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("member_teamsIncluded.html", teams=teams, member=member)


# ---------------------------------------------
# View Single Team
# ---------------------------------------------
@member_mainpage_bp.route("/member-viewTeam/<int:team_id>")
def member_view_team(team_id):
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Fetch team details
    cur.execute("""
        SELECT t.name AS team_name, t.description, u.username AS leader_name
        FROM teams t
        LEFT JOIN users u ON t.leader_id = u.user_id
        WHERE t.team_id = %s;
    """, (team_id,))
    team = cur.fetchone()

    # Fetch members
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
        return redirect(url_for("member_mainpage_bp.member_teams_included"))

    return render_template("member_viewTeam.html", team=team, members=members)


# ---------------------------------------------
# View Tasks Assigned to Member
# ---------------------------------------------
@member_mainpage_bp.route("/member-tasks")
def member_view_tasks():
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    member_email = session["member_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get member user_id
    cur.execute("SELECT user_id, username FROM users WHERE email = %s;", (member_email,))
    member = cur.fetchone()
    if not member:
        flash("Member not found.", "error")
        conn.close()
        return redirect("/member-login")

    user_id = member["user_id"]

    # Get all tasks assigned to this member (with leader name)
    cur.execute("""
        SELECT 
            t.task_id,
            t.title,
            t.description,
            t.status,
            t.priority,
            t.due_date,
            tm.name AS team_name,
            u.username AS leader_name
        FROM tasks t
        LEFT JOIN teams tm ON t.team_id = tm.team_id
        LEFT JOIN users u ON tm.leader_id = u.user_id
        WHERE t.assigned_to = %s
        ORDER BY t.due_date ASC;
    """, (user_id,))
    tasks = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("member_viewTasks.html", member=member, tasks=tasks)


# ---------------------------------------------
# View Task Details + Comments
# ---------------------------------------------
@member_mainpage_bp.route("/member-viewTask/<int:task_id>")
def member_view_task(task_id):
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # ---------------------------------------------------
    # Load task details (NO team_name)
    # ---------------------------------------------------
    cur.execute("""
        SELECT 
            t.task_id,
            t.title,
            t.description,
            t.status,
            t.priority,
            t.due_date,
            t.created_at,
            cu.username AS created_by_username,
            au.username AS assigned_to_username,
            tm.team_id,
            NULL AS team_name         -- database does NOT contain team_name
        FROM tasks t
        JOIN users cu ON t.created_by = cu.user_id
        JOIN users au ON t.assigned_to = au.user_id
        JOIN teams tm ON t.team_id = tm.team_id
        WHERE t.task_id = %s;
    """, (task_id,))
    
    task = cur.fetchone()

    if not task:
        cur.close()
        conn.close()
        flash("Task not found.", "error")
        return redirect(url_for("member_mainpage_bp.member_view_tasks"))

    # ---------------------------------------------------
    # Load comments
    # ---------------------------------------------------
    cur.execute("""
        SELECT 
            c.comment_id,
            c.content,
            c.created_at,
            u.username
        FROM comments c
        JOIN users u ON c.author_id = u.user_id
        WHERE c.task_id = %s
        ORDER BY c.created_at DESC;
    """, (task_id,))
    
    comments = cur.fetchall()

    # ---------------------------------------------------
    # Load attachments
    # ---------------------------------------------------
    cur.execute("""
        SELECT 
            attachment_id,
            file_name,
            file_path,
            comment_id
        FROM attachments
        WHERE task_id = %s;
    """, (task_id,))
    
    attachment_rows = cur.fetchall()

    attachments_by_comment = {}
    for a in attachment_rows:
        attachments_by_comment.setdefault(a["comment_id"], []).append(a)

    cur.close()
    conn.close()

    return render_template(
        "member_viewTask.html",
        task=task,
        comments=comments,
        attachments_by_comment=attachments_by_comment
    )






# ---------------------------------------------
# Add Comment (POST)
# ---------------------------------------------
@member_mainpage_bp.route("/member-addComment/<int:task_id>", methods=["POST"])
def member_add_comment(task_id):
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    content = request.form.get("content")
    file = request.files.get("file")

    if not content:
        flash("Comment cannot be empty.", "error")
        return redirect(url_for("member_mainpage_bp.member_add_comment_page", task_id=task_id))

    member_email = session["member_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Find member ID
    cur.execute("SELECT user_id FROM users WHERE email = %s;", (member_email,))
    member = cur.fetchone()
    if not member:
        flash("User not found.", "error")
        cur.close()
        conn.close()
        return redirect(url_for("member_mainpage_bp.member_add_comment_page", task_id=task_id))

    author_id = member["user_id"]

    # Insert comment and return ID
    cur.execute("""
        INSERT INTO comments (task_id, author_id, content, created_at)
        VALUES (%s, %s, %s, NOW())
        RETURNING comment_id
    """, (task_id, author_id, content))
    comment_id = cur.fetchone()["comment_id"]

    # Handle file upload
    if file and file.filename:
        filename = secure_filename(file.filename)

        if "." not in filename:
            flash("Invalid file name.", "error")
            conn.rollback()
            cur.close()
            conn.close()
            return redirect(url_for("member_mainpage_bp.member_add_comment_page", task_id=task_id))

        ext = filename.rsplit(".", 1)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            flash(f"File type .{ext} not allowed.", "error")
            conn.rollback()
            cur.close()
            conn.close()
            return redirect(url_for("member_mainpage_bp.member_add_comment_page", task_id=task_id))

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_system_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_system_path)

        db_path = os.path.join("uploads", filename)

        cur.execute("""
            INSERT INTO attachments (file_name, file_path, uploaded_by, task_id, comment_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (filename, db_path, author_id, task_id, comment_id))

    conn.commit()
    cur.close()
    conn.close()

    flash("Comment added successfully!", "success")
    return redirect(url_for("member_mainpage_bp.member_view_tasks"))



# ---------------------------------------------
# Comment Page (GET)
# ---------------------------------------------
@member_mainpage_bp.route("/member-addCommentPage/<int:task_id>")
def member_add_comment_page(task_id):
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    # Get the task to show its title in the comment page
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT title, description FROM tasks WHERE task_id = %s;", (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()

    if not task:
        flash("Task not found.", "error")
        return redirect(url_for("member_mainpage_bp.member_view_tasks"))

    return render_template("member_addComment.html", task=task, task_id=task_id)

# ---------------------------------------------
# Change Task Status (POST)
# ---------------------------------------------
@member_mainpage_bp.route("/member-changeStatus/<int:task_id>", methods=["POST"])
def member_change_status(task_id):
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    new_status = request.form.get("new_status")
    if new_status not in ("TODO", "IN_PROGRESS", "DONE"):
        flash("Invalid status.", "error")
        return redirect(url_for("member_mainpage_bp.member_view_tasks"))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("UPDATE tasks SET status = %s WHERE task_id = %s;", (new_status, task_id))
        conn.commit()
        flash(f"✅ Task status updated to {new_status}!", "success")
    except Exception as e:
        conn.rollback()
        flash(f"❌ Error updating status: {e}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for("member_mainpage_bp.member_view_tasks"))


# -------------------------------------------------
# Notifications and Deadlines
# -------------------------------------------------
@member_mainpage_bp.route("/member-notifications_and_deadlines")
def member_notifications_and_deadlines():
    if "member_email" not in session:
        flash("Please log in first.", "error")
        return redirect("/member-login")

    member_email = session["member_email"]

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Find member_id
    cur.execute("SELECT user_id FROM users WHERE email = %s;", (member_email,))
    user = cur.fetchone()
    if not user:
        flash("User not found.", "error")
        cur.close()
        conn.close()
        return redirect("/member-login")

    member_id = user["user_id"]

    # Fetch latest comments on member’s tasks (not written by themselves)
    cur.execute("""
        SELECT 
            c.content,
            c.created_at,
            u.username AS author,
            t.title AS task_title
        FROM comments c
        JOIN tasks t ON c.task_id = t.task_id
        JOIN users u ON c.author_id = u.user_id
        WHERE t.assigned_to = %s AND c.author_id <> %s
        ORDER BY c.created_at DESC
        LIMIT 10;
    """, (member_id, member_id))
    incoming_comments = cur.fetchall()

    # Fetch deadlines for assigned tasks (excluding DONE)
    cur.execute("""
        SELECT 
            title, 
            due_date, 
            status, 
            priority 
        FROM tasks
        WHERE assigned_to = %s
        AND due_date IS NOT NULL
        AND status != 'DONE'
        ORDER BY due_date ASC;
    """, (member_id,))
    active_deadlines = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "member_notifications_and_deadlines.html",
        comments=incoming_comments,
        deadlines=active_deadlines,
        email=member_email
    )
