from config import ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if uploaded file type is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
