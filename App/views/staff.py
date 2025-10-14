from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_staff,
    get_all_staff_json,
    jwt_required
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


@staff_views.route('/api/staff', methods=['GET'])
def api_get_all_staff():
    return jsonify(get_all_staff_json())