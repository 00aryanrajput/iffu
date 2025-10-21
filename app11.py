from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=os.environ.get("MYSQLPORT", 3306)
    )

    

# ---------- LOGIN ----------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return redirect(url_for('home'))
    else:
        return "<h3>Invalid username or password</h3><a href='/'>Try Again</a>"

# ---------- HOME ----------
@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('final_home.html', username=session['username'])

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    text = request.form.get('feelingText', '')

    file = request.files.get('file')

    if file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        file_type = 'image' if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')) else 'video'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gallery (text_content, file_path, file_type, upload_date) VALUES (%s, %s, %s, %s)",
            (text, filename, file_type, datetime.now())
        )
        conn.commit()
        conn.close()

    return redirect(url_for('gallery'))

# ---------- GALLERY ----------
@app.route('/gallery')
def gallery():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM gallery ORDER BY upload_date DESC")
    files = cursor.fetchall()
    conn.close()

    return render_template('gallery1.html', files=files)

@app.route('/delete', methods=['POST'])
def delete():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get selected IDs
    ids_to_delete = request.form.getlist('delete_ids')  # list of IDs

    if ids_to_delete:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        for file_id in ids_to_delete:
            # Get file path from DB
            cursor.execute("SELECT file_path FROM gallery WHERE id=%s", (file_id,))
            file = cursor.fetchone()
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file['file_path'])
                # Remove file from system
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Remove from DB
                cursor.execute("DELETE FROM gallery WHERE id=%s", (file_id,))
        conn.commit()
        conn.close()

    return redirect(url_for('gallery'))


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

