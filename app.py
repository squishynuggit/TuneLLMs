import os
from flask import Flask, request, redirect, url_for, render_template, flash

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}
app.config['SECRET_KEY'] = 'supersecretkey'

# Ensure the main upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_and_list_files():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            if os.path.exists(file_path):
                flash('File already exists.')
            else:
                file.save(file_path)
                flash('File successfully uploaded')
        else:
            flash('Allowed file types are: pdf, txt, docx')
    
    # List files in the main upload directory
    files = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
    
    # Render the upload form and file list
    return render_template('upload.html', files=files)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f'File {filename} deleted successfully.')
    else:
        flash(f'File {filename} not found.')

    return redirect(url_for('upload_and_list_files'))

if __name__ == "__main__":
    app.run(debug=True)
