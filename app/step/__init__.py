from flask import Blueprint

step = Blueprint('step', __name__);

from . import views