from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")

# Cloudinary config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)
print("Cloudinary keys:", 
      os.getenv("CLOUDINARY_CLOUD_NAME"), 
      os.getenv("CLOUDINARY_API_KEY"), 
      os.getenv("CLOUDINARY_API_SECRET"))

# Upload folder (temporary local save)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    return conn

# ---------- LOGIN ----------
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
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

# ---------- UPLOAD ----------
@app.route('/upload', methods=['POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login')) 

    text_content = request.form.get('feelingText', '')
    file = request.files.get('file')

    if not file:
        return "No file selected", 400

    filename = secure_filename(file.filename)
    file_type = 'image' if filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'webp')) else 'video'

    # ✅ Create temporary path (Render pe static/uploads folder writable nahi hota)
    temp_path = os.path.join('/tmp', filename)
    file.save(temp_path)

    try:
        # ✅ Upload to Cloudinary directly from temporary path
        upload_result = cloudinary.uploader.upload(temp_path, resource_type="auto")
        os.remove(temp_path)

        # ✅ Save only the Cloudinary URL in database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO gallery (text_content, file_path, file_type)
            VALUES (%s, %s, %s)
        """, (text_content, upload_result['secure_url'], file_type))
        conn.commit()
        conn.close()

        return redirect(url_for('gallery'))

    except Exception as e:
        print("Upload failed:", e)
        return f"Error: {e}", 500

# ---------- GALLERY ----------
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

# ---------- DELETE ----------
@app.route('/delete', methods=['POST'])
def delete():
    if 'username' not in session:
        return redirect(url_for('login'))

    ids_to_delete = request.form.getlist('delete_ids')
    if ids_to_delete:
        conn = get_db_connection()
        cursor = conn.cursor()
        for file_id in ids_to_delete:
            cursor.execute("SELECT file_path FROM gallery WHERE id=%s", (file_id,))
            file = cursor.fetchone()
            if file:
                # Delete from Cloudinary
                public_id = file[0].split('/')[-1].split('.')[0]
                try:
                    cloudinary.uploader.destroy(public_id, resource_type="auto")
                except Exception as e:
                    print("Cloudinary Delete Error:", e)
                # Delete from DB
                cursor.execute("DELETE FROM gallery WHERE id=%s", (file_id,))
        conn.commit()
        conn.close()

    return redirect(url_for('gallery'))

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ---------- RUN APP ----------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
