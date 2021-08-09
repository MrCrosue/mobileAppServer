from flask import Blueprint

geo_bp = Blueprint('geo', __name__)

from app.geo import routes