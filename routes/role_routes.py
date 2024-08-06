from flask import Blueprint, request, render_template, redirect, url_for
import mysql.connector
from models import get_db_connection

role_bp = Blueprint('role_bp', __name__)

@role_bp.route('/roles')
def list_roles():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('role_management.html', roles=roles)

@role_bp.route('/roles/add', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        role_name = request.form['role_name']
        privileges = request.form['privileges']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO roles (role_name, privileges)
        VALUES (%s, %s)
        ''', (role_name, privileges))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('role_bp.list_roles'))
    return render_template('role_management.html')

@role_bp.route('/roles/delete/<int:id>')
def delete_role(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM roles WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('role_bp.list_roles'))
