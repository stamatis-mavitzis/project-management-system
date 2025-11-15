from flask import Flask, request, render_template, redirect, url_for, flash, session  # type: ignore
from psycopg2.extras import RealDictCursor  # type: ignore
from werkzeug.utils import secure_filename  # type: ignore
from datetime import datetime

# Import Config and Database Connection
from config import SECRET_KEY, UPLOAD_FOLDER

# Import Blueprints
from routes.homepage import homepage_bp
from routes.admin_teamLeader_member_options import admin_teamLeader_member_options_bp
from routes.admin_authenticate import admin_authenticate_bp
from routes.teamLeader_authenticate import teamLeader_authenticate_bp
from routes.member_authenticate import member_authenticate_bp
from routes.admin_mainpage import admin_mainpage_bp
from routes.teamLeader_mainpage import teamLeader_mainpage_bp
from routes.member_mainpage import member_mainpage_bp

# ---------------------------------------------
# --- Initialize Flask App and Configuration ---
# ---------------------------------------------
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Add global date formatting filter before app runs
@app.template_filter('format_date')
def format_date(value):
    """Formats a datetime/date value as dd/mm/yyyy."""
    if not value:
        return "—"
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.strftime("%d/%m/%Y")
    except Exception:
        return str(value)

# ---------------------------------------------
# --- Register Blueprints ---
# ---------------------------------------------
app.register_blueprint(homepage_bp)
app.register_blueprint(admin_teamLeader_member_options_bp)
app.register_blueprint(admin_authenticate_bp)
app.register_blueprint(teamLeader_authenticate_bp)
app.register_blueprint(member_authenticate_bp)
app.register_blueprint(admin_mainpage_bp)
app.register_blueprint(teamLeader_mainpage_bp)
app.register_blueprint(member_mainpage_bp)


# --------------------------------------------------
# --- Fix for old template endpoints (no prefix) ---
# --------------------------------------------------
def add_aliases(app):
    """
    Re-registers blueprint routes under old endpoint names
    so url_for('add_to_cart') etc. continue to work.
    """
    for rule in list(app.url_map.iter_rules()):
        if rule.endpoint.startswith("admin."):
            short_endpoint = rule.endpoint.split("admin.", 1)[1]
            if short_endpoint not in app.view_functions:
                app.add_url_rule(
                    rule.rule,
                    endpoint=short_endpoint,
                    view_func=app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
        if rule.endpoint.startswith("teamLeader."):
            short_endpoint = rule.endpoint.split("teamLeader.", 1)[1]
            if short_endpoint not in app.view_functions:
                app.add_url_rule(
                    rule.rule,
                    endpoint=short_endpoint,
                    view_func=app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
        if rule.endpoint.startswith("member."):
            short_endpoint = rule.endpoint.split("member.", 1)[1]
            if short_endpoint not in app.view_functions:
                app.add_url_rule(
                    rule.rule,
                    endpoint=short_endpoint,
                    view_func=app.view_functions[rule.endpoint],
                    methods=rule.methods
                )
    print("Old client endpoints successfully restored.")


# Run this after all blueprints are registered
add_aliases(app)

# ---------------------------------------------
# --- Run App ---
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
