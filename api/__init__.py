from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

from . import teams
from . import stadiums
from . import lobbies
from . import tournaments