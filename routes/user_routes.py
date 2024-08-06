from flask import Blueprint, request, render_template, redirect, url_for
import mysql.connector
from models import get_db_connection

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users')
def list_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('user_management.html', users=users)

@user_bp.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        mobile_number = request.form['mobile_number']
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO users (first_name, last_name, email, mobile_number, username, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (first_name, last_name, email, mobile_number, username, password))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('user_bp.list_users'))
    return render_template('user_management.html')

@user_bp.route('/users/delete/<int:id>')
def delete_user(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('user_bp.list_users'))
