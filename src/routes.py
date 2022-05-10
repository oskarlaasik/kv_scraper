from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import func
from sqlalchemy.orm import aliased

from src import db

api_bp = Blueprint('api', __name__)

@api_bp.route('/api')
def api():
    return render_template('documentation.html')

