from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers.staff_controller import get_all_staff_json
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Student

from.index import index_views

from App.controllers import (
    create_user,
    get_all_students,
    get_all_students_json,
    jwt_required
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')


@student_views.route('/api/students', methods=['GET'])
def api_get_all_students():
    return jsonify(get_all_students_json())

@student_views.route('/api/view_accolades', methods=['GET'])
@jwt_required()
def api_view_accolades():
    user = jwt_current_user
    student = Student.query.filter_by(user_id=user.id).first()
    if not student:
        return jsonify({"error": "Only students are allowed to view their own accolades"}), 404
    accolades = student.accolades()
    return jsonify(accolades)

