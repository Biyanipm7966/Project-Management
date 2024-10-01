from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load the project data from JSON
def load_project_data():
    with open('project_data.json') as f:
        return json.load(f)

# Save the project data to JSON
def save_project_data(data):
    with open('project_data.json', 'w') as f:
        json.dump(data, f)

@app.route('/')
def dashboard():
    project_data = load_project_data()
    return render_template('dashboard.html', project_data=project_data)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/aoa')
def aoa():
    return render_template('aoa.html')

@app.route('/wbs_mindmap')
def wbs_mindmap():
    return render_template('wbs_mindmap.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

if __name__ == '__main__':
    app.run(debug=True)
