from flask import request, jsonify, make_response
from flask_cors import cross_origin
from app import app
import service.authService as authService


@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    email, username, password = request.form.get('email'), request.form.get('username'), request.form.get('password')
    authService.handleRegisterRequest(email, username, password)
    return "ok"


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    emailOrUsername, password = request.form.get('login'), request.form.get('password')
    try:
        token = authService.handleLogin(emailOrUsername, emailOrUsername, password)
        return jsonify({'token': token})
    except:
        return make_response({'message': "BAD_CREDENTIALS"}, 400)
