from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Database Connection
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"), sslmode="require")
    return conn


# -------------------- ROUTES -----------------------

@app.route('/')
def home():
    return render_template('final_home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('gallery'))
        else:
            return "<h3>Invalid credentials. Please try again.</h3>"

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/gallery')
def gallery():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gallery ORDER BY upload_date DESC")
    rows = cursor.fetchall()
    conn.close()

    files = []
    for row in rows:
        files.append({
            'id': row[0],
            'text_content': row[1],
            'file_path': row[2],
            'file_type': row[3],
            'upload_date': row[4]
        })

    return render_template('gallery1.html', files=files)


# -------------------- FIXED UPLOAD ROUTE -----------------------

@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    text = request.form.get('feelingText', '')
    file = request.files.get('file')

    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Detect resource type manually
            file_ext = filename.split('.')[-1].lower()
            if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
                resource_type = 'image'
            elif file_ext in ['mp4', 'mov', 'avi', 'webm']:
                resource_type = 'video'
            else:
                return "<h3>Unsupported file type!</h3>"

            upload_result = cloudinary.uploader.upload(
                filepath,
                resource_type=resource_type
            )
            cloudinary_url = upload_result['secure_url']

        except Exception as e:
            print("Cloudinary Upload Error:", e)
            return "<h3>File upload failed. Check Cloudinary credentials or file type.</h3>"

        # Insert into DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gallery (text_content, file_path, file_type, upload_date) VALUES (%s, %s, %s, %s)",
            (text, cloudinary_url, resource_type, datetime.now())
        )
        conn.commit()
        conn.close()

        # Delete local temp file
        if os.path.exists(filepath):
            os.remove(filepath)

    return redirect(url_for('gallery'))


@app.route('/delete', methods=['POST'])
def delete():
    if 'username' not in session:
        return redirect(url_for('login'))

    ids = request.form.getlist('selected_files')
    if ids:
        conn = get_db_connection()
        cursor = conn.cursor()
        for file_id in ids:
            cursor.execute("DELETE FROM gallery WHERE id=%s", (file_id,))
        conn.commit()
        conn.close()

    return redirect(url_for('gallery'))


# -------------------- MAIN -----------------------

if __name__ == "__main__":
    app.run(debug=True)

