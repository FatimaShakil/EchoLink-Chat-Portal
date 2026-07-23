import os
import logging
from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory
from flask_socketio import SocketIO, send, emit, disconnect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from ftplib import FTP
from datetime import datetime
from flask import jsonify
from flask import flash, redirect, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
socketio = SocketIO(app)
db = SQLAlchemy(app)

log_folder = 'logs'
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logging.basicConfig(filename=os.path.join(log_folder, 'activity.log'), level=logging.INFO)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

active_users = {}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat')) 
    return redirect(url_for('login')) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            logging.info(f'{username} logged in at {datetime.now()}')
            return redirect(url_for('chat'))
        else:
            return "Invalid Credentials!", 401
    return render_template('login.html')

@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        username = session['username']
        active_users[request.sid] = username
        logging.info(f'{username} connected with session ID {request.sid}')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    join_message = f'{username} has joined the chat.'
    logging.info(join_message)
    emit('join_announcement', join_message, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in active_users:
        username = active_users[request.sid]
        del active_users[request.sid]
        leave_message = f'{username} has left the chat.'
        logging.info(leave_message)
        emit('leave_announcement', leave_message, broadcast=True)


@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        logging.info(f'{username} logged out at {datetime.now()}')
    session.pop('username', None)  
    return redirect(url_for('login')) 


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect('/register')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')


@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])


@socketio.on('message')
def handle_message(msg):
    username = session['username']
    formatted_message = f'{username}: {msg}' 
    logging.info(f'Message from {username}: {msg} at {datetime.now()}')
    send(formatted_message, broadcast=True) 

ftp = FTP()
ftp_host = "127.0.0.1"  
ftp_port = 2121 
ftp_user = "user"
ftp_password = "password"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'username' not in session:
        return jsonify(success=False, error="Not logged in"), 401
    file = request.files.get('file')
    if not file:
        return jsonify(success=False, error="No file selected!"), 400 
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = file.filename
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        try:
            ftp.connect(ftp_host, ftp_port)
            ftp.login(ftp_user, ftp_password)
            with open(filepath, 'rb') as f:
                ftp.storbinary(f"STOR {filename}", f)
            ftp.quit()
            logging.info(f"File uploaded by {session['username']} at {datetime.now()} to FTP")
        except Exception as e:
            logging.error(f"FTP upload failed: {str(e)}")
            
        return jsonify(success=True, filename=filename)
    except Exception as e:
        logging.error(f"File upload failed: {str(e)}")
        return jsonify(success=False, error=f"Upload failed: {str(e)}"), 500


@app.route('/download/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))
    file_path = os.path.join('uploads', filename)

    if os.path.exists(file_path):
        logging.info(f"File '{filename}' downloaded by {session['username']} at {datetime.now()}")
        return send_from_directory('uploads', filename, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5001, debug=True)