from flask import Flask, render_template
from project_data import project_info
from diagrams import create_gantt_chart, create_wbs_diagram, create_aoa_diagram

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html', project=project_info)

@app.route('/calendar')
def calendar():
    gantt_chart_url = create_gantt_chart()
    return render_template('calendar.html', gantt_chart=gantt_chart_url)

@app.route('/wbs_mindmap')
def wbs_mindmap():
    wbs_diagram_url = create_wbs_diagram()
    return render_template('wbs_mindmap.html', wbs_diagram=wbs_diagram_url)

@app.route('/aoa_diagram')
def aoa_diagram():
    aoa_diagram_url = create_aoa_diagram()
    return render_template('aoa_diagram.html', aoa_diagram=aoa_diagram_url)

if __name__ == "__main__":
    app.run(debug=True)
