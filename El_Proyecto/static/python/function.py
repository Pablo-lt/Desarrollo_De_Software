from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4', 'webm', 'ogg', 'mp3', 'wav'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = file.filename
            target_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(target_path)
            return redirect(url_for('index'))

    files = os.listdir(UPLOAD_FOLDER)
    media_files = []
    for file in files:
        file_ext = file.rsplit('.', 1)[1].lower()
        media_files.append({'name': file, 'ext': file_ext})

    return render_template('index.html', media_files=media_files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
