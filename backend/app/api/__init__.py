# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

from .array import *
from .iops import *


@api.errorhandler(404)
def handle_not_found(e):
    return jsonify({
        'error': 'Not found'
    }), 404
