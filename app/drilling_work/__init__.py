from flask import Blueprint

drilling_work_bp = Blueprint('drilling_work_bp', __name__)

from app.drilling_work import routes