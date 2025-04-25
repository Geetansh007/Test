from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
import uuid
from ..models import User, db
from ..utils.helpers import encrypt_data

class OpsUserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email, is_ops_user=True).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        if not user.is_verified:
            return {'message': 'Email not verified'}, 403

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'is_ops_user': True}
        )
        return {'access_token': access_token}, 200

class ClientUserSignup(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 400

        user = User(email=email, is_ops_user=False)
        user.set_password(password)
        
        verification_token = str(uuid.uuid4())
        user.verification_token = verification_token
        
        db.session.add(user)
        db.session.commit()

        verification_url = f"http://example.com/verify-email?token={verification_token}"
        encrypted_url = encrypt_data(verification_url)
        
        return {
            'message': 'User created successfully. Verification email sent.',
            'encrypted_url': encrypted_url
        }, 201

class ClientUserVerify(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('token')

        user = User.query.filter_by(verification_token=token, is_ops_user=False).first()
        if not user:
            return {'message': 'Invalid or expired token'}, 400

        user.is_verified = True
        user.verification_token = None
        db.session.commit()

        return {'message': 'Email verified successfully'}, 200

class ClientUserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email, is_ops_user=False).first()
        if not user or not user.check_password(password):
            return {'message': 'Invalid credentials'}, 401

        if not user.is_verified:
            return {'message': 'Email not verified'}, 403

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'is_ops_user': False}
        )
        return {'access_token': access_token}, 200