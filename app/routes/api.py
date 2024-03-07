from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()

    try:
        newUser = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password')
        )
        db.add(newUser)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return jsonify(message='Signup failed'), 500

    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True

    return jsonify(id=newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter(User.email == data.get('email')).one()
        if user.verify_password(data.get('password')):
            session.clear()
            session['user_id'] = user.id
            session['loggedIn'] = True
            return jsonify(id=user.id)
        else:
            return jsonify(message='Incorrect credentials'), 400
    except Exception as e:
        print(e)
        return jsonify(message='Incorrect credentials'), 400
