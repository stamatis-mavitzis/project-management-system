from flask import Blueprint, render_template # type: ignore

homepage_bp = Blueprint("homepage", __name__)

# ---------------------------------------------
# --- Home Page ---
# ---------------------------------------------
@homepage_bp.route("/")
def index():
    """Renders the homepage."""
    return render_template("index.html")
 
   