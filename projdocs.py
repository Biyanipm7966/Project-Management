from flask import send_file

@app.route('/documents')
def documents():
    return render_template('documents.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join('uploads', file.filename))
    return 'File uploaded successfully'
