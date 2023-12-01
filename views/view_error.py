from flask import Blueprint, render_template

view_error_bp = Blueprint('view_error_bp', __name__)


@view_error_bp.route('/view_error', methods=['GET'])
def view_error():
    return render_template("error.html")