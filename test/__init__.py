from flask import Flask
from .config import Config
from .extensions import db, jwt
from .resources.auth import OpsUserLogin, ClientUserSignup, ClientUserVerify, ClientUserLogin
from .resources.files import FileUpload, FileList, FileDownload, SecureFileDownload

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints or resources
    api = Api(app)
    
    # Auth routes
    api.add_resource(OpsUserLogin, '/ops/login')
    api.add_resource(ClientUserSignup, '/client/signup')
    api.add_resource(ClientUserVerify, '/client/verify')
    api.add_resource(ClientUserLogin, '/client/login')
    
    # File routes
    api.add_resource(FileUpload, '/upload')
    api.add_resource(FileList, '/files')
    api.add_resource(FileDownload, '/download-file/<int:file_id>')
    api.add_resource(SecureFileDownload, '/download-file/<string:uuid_name>')

    return app