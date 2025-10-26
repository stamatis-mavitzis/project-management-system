from flask import Blueprint, render_template # type: ignore

admin_teamLeader_member_options_bp = Blueprint("admin_teamLeader_member_options", __name__)

# ---------------------------------------------
# --- Admin or Team Leader or Member Selection ---
# ---------------------------------------------
@admin_teamLeader_member_options_bp.route("/admin-or-teamLeader-or-member")
def client_or_salesman():
    """Page for choosing between admin team Leader or member login."""
    return render_template("admin_or_teamLeader_or_member.html")

# ---------------------------------------------
# --- Options Page ---
# ---------------------------------------------
@admin_teamLeader_member_options_bp.route("/admin-options")
def admin_options():
    """Page for admin login or signup options."""
    return render_template("admin_signin_or_login.html")

@admin_teamLeader_member_options_bp.route("/teamLeader-options")
def teamLeader_options():
    """Page for teamLeader login or signup options."""
    return render_template("teamLeader_signin_or_login.html")

@admin_teamLeader_member_options_bp.route("/member-options")
def memberr_options():
    """Page for member login or signup options."""
    return render_template("member_signin_or_login.html")