from flask import Blueprint

ui = Blueprint('ui', __name__, url_prefix='/', template_folder='templates')

from . import views