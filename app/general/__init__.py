from flask import Blueprint

general_bp = Blueprint('general_bp', __name__)

from app.general import routes