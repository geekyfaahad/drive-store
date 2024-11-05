from flask import Flask, request, redirect, session, abort, render_template, send_from_directory, url_for
from flask_compress import Compress
from werkzeug.utils import secure_filename
import os
from markupsafe import Markup
import pyrebase
from func import *
config  = {
  "apiKey": "AIzaSyBP48OmUEnHzTLAp07n-sQLrylaut-hDkM",
  "authDomain": "nextbox-395f3.firebaseapp.com",
  "databaseURL":"https://nextbox-395f3-default-rtdb.firebaseio.com",
  "projectId": "nextbox-395f3",
  "storageBucket": "nextbox-395f3.appspot.com",
  "messagingSenderId": "176855469944",
  "appId": "1:176855469944:web:71a36c1d1fccbf679b028d"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
UPLOAD_FOLDER = 'cloud'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' , 'mp4', 'mkv', 'zip'}


app = Flask(__name__)
Compress(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024  # 10GB max upload size
app.secret_key = "hhhj875466@_765g98787hfyfh87"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    masthead = generate_header()
    if 'user' in session:
        mypath = os.path.join(app.config.get('UPLOAD_FOLDER', ''), session['user'], 'files')
        os.makedirs(mypath, exist_ok=True)
        files = os.listdir(mypath)
        return render_template('profile.html', files=files, h=masthead, user=session['user'])
    
    if request.method == 'POST':
        email = request.form.get('usrname')
        password = request.form.get('ps')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            session['token'] = user['idToken']
            
            mypath = os.path.join(app.config.get('UPLOAD_FOLDER', ''), session['user'], 'files')
            os.makedirs(mypath, exist_ok=True)
            files = os.listdir(mypath)
            return render_template('profile.html', user=session['user'], files=files, h=masthead)
        
        except Exception as e:
            error_message = Markup("<script>window.onload = function() { incorrect_text(); };</script>")
            app.logger.error(f"Login error: {e}")
            return render_template("index.html", error=error_message)

    return render_template('index.html')


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form.get('usrname')
        try:
            auth.send_password_reset_email(email)
            reset_message = Markup("<script>window.onload = function() { reset_text(); };</script>")
        except Exception as e:
            message = "Failed to Reset"
            app.logger.error(f"Password reset error: {str(e)}")
        return render_template("reset.html", message=reset_message)
    return render_template("reset.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('usrnme')
        password = request.form.get('ps')
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            verify_message = Markup("<script>window.onload = function() { verify_text(); };</script>")
            return render_template("register.html",h=verify_message)
        except Exception as e:
            error_message = Markup("<script>window.onload = function() { alert_text(); };</script>")
            return render_template("register.html", error=error_message)
    return render_template("register.html")

@app.route('/create', methods=['POST'])
def create():
    if 'user' not in session:
        abort(403)
    directory = request.json.get('hk8')
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    path = os.path.join(user_dir, directory)
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        app.logger.error(f"Error creating directory: {error}")
        abort(500)
    return redirect(url_for("index"))

@app.route('/upload/<path:folder_path>', methods=['POST'])
def upload(folder_path):
    if 'user' not in session:
        abort(403)
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    upload_path = os.path.normpath(os.path.join(user_dir, folder_path))
    if not upload_path.startswith(user_dir):
        abort(403)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    files = request.files.getlist("file-input[]")
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_path, filename)
            file.save(file_path)
    return redirect(url_for('dynamic', folder_path=folder_path))

@app.route('/folder/delete/<path:folder_path>', methods=['GET'])
def folder_delete(folder_path):
    if 'user' not in session:
        abort(403)
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    full_path = os.path.normpath(os.path.join(user_dir, folder_path))

    if not full_path.startswith(user_dir):
        abort(403) 

    if os.path.isdir(full_path):
        for root, dirs, files in os.walk(full_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name)) 
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(full_path) 
        app.logger.info(f"Directory and all its contents deleted: {full_path}")
        message=Markup("<script>window.onload = function() { delete_folder(); };</script>")
        return render_template('profile.html',message=message)
    else:
        app.logger.warning(f"Path not found or not a directory: {full_path}")
        return f"The specified path '{folder_path}' does not exist or is not a directory.", 404

@app.route('/f/<path:folder_path>')
def dynamic(folder_path):
    if 'user' not in session:
        return redirect(url_for('index'))
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    full_path = os.path.normpath(os.path.join(user_dir, folder_path))
    if not full_path.startswith(user_dir):
        abort(403) 
    if not os.path.isdir(full_path):
        abort(404)
    files = os.listdir(full_path)
    masthead= generate_header()
    return render_template('files.html', user=session['user'],files=files, folder_path=folder_path)

@app.route('/file/download/<path:folder_path>/<filename>')
def download_file(folder_path, filename):
    if 'user' not in session:
        abort(403)
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    file_path = os.path.normpath(os.path.join(user_dir, folder_path, filename))
    if not file_path.startswith(user_dir):
        abort(403)
    if not os.path.isfile(file_path):
        abort(404)
    return send_from_directory(os.path.dirname(file_path), filename)

@app.route('/file/delete/<path:folder_path>/<filename>')
def remove_file(folder_path, filename):
    if 'user' not in session:
        abort(403)
    user_dir = os.path.join(app.config['UPLOAD_FOLDER'], session['user'], 'files')
    file_path = os.path.normpath(os.path.join(user_dir, folder_path, filename))
    if not file_path.startswith(user_dir):
        abort(403)
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        app.logger.warning(f"File not found: {file_path}")
    return redirect(url_for('dynamic', folder_path=folder_path))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=4000, host='0.0.0.0')
    # app.run(ssl_context='adhoc')  # For HTTPS; use your SSL certificates in production