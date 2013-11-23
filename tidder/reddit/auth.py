"""Reddit authentication"""

from . import api


def login(username, password):
    api.login(username, password)
