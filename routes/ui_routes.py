from flask import Blueprint, request, render_template, redirect, url_for
import mysql.connector
import os
from werkzeug.utils import secure_filename
from models import get_db_connection
from config import Config

ui_bp = Blueprint('ui_bp', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ui_bp.route('/custom-ui', methods=['GET', 'POST'])
def custom_ui():
    if request.method == 'POST':
        color = request.form.get('color')
        logo = request.files.get('logo')
        logo_path = None
        
        if logo and allowed_file(logo.filename):
            filename = secure_filename(logo.filename)
            logo_path = os.path.join('images', filename)
            logo.save(os.path.join('static', logo_path))
            print(f"Logo saved at: {os.path.join('static', logo_path)}")  # Debugging output
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO settings (color, logo_path)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE color=%s, logo_path=%s
        ''', (color, logo_path, color, logo_path))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('ui_bp.custom_ui'))
    
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM settings LIMIT 1")
    settings = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('custom_ui.html', settings=settings)
