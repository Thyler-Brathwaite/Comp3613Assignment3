from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.models import Staff, Request
from App.controllers.staff_controller import fetch_all_requests, process_request_approval, process_request_denial
from.index import index_views
from App import db
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

@staff_views.route('/api/approve_request', methods=['PUT'])
@jwt_required()
def api_approve_request():
    user = jwt_current_user
    staff = Staff.query.filter_by(user_id=user.id).first()
    if not staff:
        return jsonify({"error": "Only staff are allowed to approve hours requests"}), 404
    
    data = request.form
    request_id = data.get('request_id')
    if not request_id:
        return jsonify({"error": "Missing request_id"}), 400
    
    req = Request.query.get(request_id)
    if not req:
        return jsonify({"error": f"Request with id {request_id} not found."}), 404
    
    status = data.get('status')
    if status == 'approved':
        req.status = 'approved'
        db.session.commit()
        return jsonify({"message": f"Request {request_id} processed", "status": req.status}), 200
    elif status == 'denied':
        req.status = 'denied'
        db.session.commit()
        return jsonify({"message": f"Request {request_id} processed", "status": req.status}), 200
    else:
        return jsonify({"error": "Invalid status value"}), 400