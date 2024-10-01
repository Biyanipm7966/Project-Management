from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        project_name = request.form['project_name']
        description = request.form['description']
        team = request.form['team']
        status = request.form['status']
        session['project'] = {
            'project_name': project_name,
            'description': description,
            'team': team,
            'status': status
        }
        return render_template('dashboard.html', project=session['project'])
    
    return render_template('dashboard.html', project=session.get('project'))

@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        if 'events' not in session:
            session['events'] = []
        session['events'].append({'title': title, 'date': date})
    return render_template('calendar.html')
