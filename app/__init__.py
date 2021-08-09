from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import logging.handlers



app = Flask(__name__)

handler = logging.handlers.RotatingFileHandler(
        'log.txt',
        maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)



app.config.from_object(Config)
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.geo import geo_bp
from app.general import general_bp
from app.drilling_work import drilling_work_bp
app.register_blueprint(geo_bp)
app.register_blueprint(general_bp)
app.register_blueprint(drilling_work_bp)


from app import models, errors
