import os
import uuid
from flask_restful import Resource
from flask import request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models import File, db
from ..utils.helpers import allowed_file, secure_filename_wrapper, encrypt_data
from ..utils.decorators import ops_user_required, client_user_required

class FileUpload(Resource):
    @jwt_required()
    @ops_user_required
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400
        
        if not allowed_file(file.filename):
            return {'message': 'Only pptx, docx, and xlsx files are allowed'}, 400

        filename = secure_filename_wrapper(file.filename)
        uuid_name = str(uuid.uuid4())
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uuid_name)
        file.save(file_path)

        current_user_id = get_jwt_identity()
        new_file = File(
            filename=filename,
            uuid_name=uuid_name,
            uploaded_by=current_user_id
        )
        db.session.add(new_file)
        db.session.commit()

        return {'message': 'File uploaded successfully', 'file_id': new_file.id}, 201

class FileList(Resource):
    @jwt_required()
    @client_user_required
    def get(self):
        files = File.query.all()
        return {
            'files': [{
                'id': file.id,
                'filename': file.filename,
                'uploaded_at': file.uploaded_at.isoformat(),
                'download_count': file.download_count
            } for file in files]
        }, 200

class FileDownload(Resource):
    @jwt_required()
    @client_user_required
    def get(self, file_id):
        file = File.query.get(file_id)
        if not file:
            return {'message': 'File not found'}, 404

        download_token = str(uuid.uuid4())
        download_url = f"/download-file/{file.uuid_name}?token={download_token}"
        encrypted_url = encrypt_data(download_url)
        
        return {
            'download-link': encrypted_url,
            'message': 'success'
        }, 200

class SecureFileDownload(Resource):
    @jwt_required()
    @client_user_required
    def get(self, uuid_name):
        token = request.args.get('token')
        if not token:
            return {'message': 'Token required'}, 403

        file = File.query.filter_by(uuid_name=uuid_name).first()
        if not file:
            return {'message': 'File not found'}, 404

        file.download_count += 1
        db.session.commit()

        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uuid_name)
        return send_from_directory(
            directory=os.path.dirname(file_path),
            path=os.path.basename(file_path),
            as_attachment=True,
            download_name=file.filename
        )