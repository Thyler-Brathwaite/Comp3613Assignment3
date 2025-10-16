from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from App.models import Staff, User, Student

from.index import index_views

from App.controllers import (
    login,
    register_student,
    register_staff
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




'''
Page/Action Routes
'''    

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    
    response = redirect(request.referrer)
    if not token:
        flash('Bad username or password', 401)
    else:
        flash('Login Successful', 201)
        set_access_cookies(response, token) 
    return response

@auth_views.route('/authorize/<user_id>', methods=['GET'])
@jwt_required()
def authorize_action(user_id):
    user_id = int(user_id)
    staff = Staff.query.all()
    students = Student.query.all()
    for st in staff:
        if st.user_id == user_id:
            user = User.query.get(user_id)
            return jsonify(message=f"User {user.username} authorized as staff")

    for st in students:
        if st.user_id == user_id:
            user = User.query.get(user_id)
            return jsonify(message=f"User {user.username} authorized as student")
    
    return jsonify(message="No matching staff or student record found"), 404

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/create_student', methods=['POST'])
def create_student_page():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    user_id = data.get('user_id')
    if not name or not email or not user_id:
        return jsonify(message="Missing required fields"), 401
    
    user_id = int(user_id)
    user = User.query.get(user_id)
    if not user:
        return jsonify(message="User not found"), 404
    
    register_student(name, email,user_id)
    return jsonify(message=f"Student created successfully!"), 200
    


@auth_views.route('/create_staff', methods=['POST'])
def create_staff_page():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    user_id = data.get('user_id')
    if not name or not email or not user_id:
        flash("Missing required fields: name, email, user_id")
        return jsonify(message="Missing required fields"), 401
    user_id = int(user_id)
    user = User.query.get(user_id)
    if not user:
        flash(f"No user found with id {user_id}")
        return jsonify(message="User not found"), 404
    register_staff(name, email, user_id)
    return jsonify(message=f"Staff created successfully!"), 200

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response