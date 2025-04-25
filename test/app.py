from fileshare_app import create_app
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Ensure upload folder exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Create database tables
        db.create_all()
    app.run(debug=True)