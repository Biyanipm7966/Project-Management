from flask import Flask, render_template
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar

# Initialize Flask app
app = Flask(__name__)

# Sample project data
dashboard_data = {
    'project_name': 'UC Punch Card',
    'project_logo': 'https://example.com/logo.png',
    'status': 'On Track',
    'milestones': [
        {'name': 'Kickoff', 'date_from': '2024-09-24', 'date_to': '2024-09-24', 'status': 'Completed'},
        {'name': 'Brainstorming', 'date_from': '2024-09-25', 'date_to': '2024-10-08', 'status': 'Completed'},
        {'name': 'Development', 'date_from': '2024-10-09', 'date_to': '2024-10-29', 'status': 'In-Progress'},
        {'name': 'Testing and Quality Assurance', 'date_from': '2024-10-30', 'date_to': '2024-11-12', 'status': 'Scheduled'},
        {'name': 'Finalizing', 'date_from': '2024-11-13', 'date_to': '2024-11-26', 'status': 'Scheduled'},
        {'name': 'Release', 'date_from': '2024-11-27', 'date_to': '2024-11-27', 'status': 'Scheduled'},
    ]
}

# Convert milestones to a pandas DataFrame
df = pd.DataFrame(dashboard_data['milestones'])

# Initialize Dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Dash App layout
dash_app.layout = html.Div([
    html.Div(id='calendar-container', style={'margin-bottom': '40px'}),
    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Input(id='task-name', type='text', placeholder='Task Name', required=True), width=4),
            dbc.Col(dbc.Input(id='start-date', type='date', placeholder='Start Date', required=True), width=2),
            dbc.Col(dbc.Input(id='end-date', type='date', placeholder='End Date', required=True), width=2),
            dbc.Col(dbc.Button("Add Task", id='add-task-btn', color='primary', n_clicks=0), width=2)
        ], className='mb-3'),
    ]),
    dcc.Graph(id='gantt-chart'),
    html.Div(id='calendar-div')
])

# Callback to add new tasks to the DataFrame and update Gantt Chart and Calendar
@dash_app.callback(
    [Output('gantt-chart', 'figure'),
     Output('calendar-div', 'children'),
     Output('calendar-container', 'children')],
    Input('add-task-btn', 'n_clicks'),
    [State('task-name', 'value'),
     State('start-date', 'value'),
     State('end-date', 'value')]
)
def update_gantt_chart(n_clicks, task_name, start_date, end_date):
    global df
    if n_clicks > 0 and task_name and start_date and end_date:
        # Ensure task name, start date, and end date are provided and valid
        try:
            # Parse the date values to ensure they are in a valid format
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            # Check if the end date is after or equal to the start date
            if end_date >= start_date:
                new_row = {'name': task_name, 'date_from': start_date, 'date_to': end_date, 'status': 'Pending'}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        except ValueError:
            pass  # If dates are invalid, skip adding the task

    # Convert 'date_from' and 'date_to' to datetime format if they are not already
    df['date_from'] = pd.to_datetime(df['date_from'])
    df['date_to'] = pd.to_datetime(df['date_to'])

    # Handle zero-duration tasks (same start and end dates) by giving them a small duration
    df['date_to'] = df.apply(
        lambda row: row['date_to'] if row['date_to'] > row['date_from'] else row['date_from'] + pd.Timedelta(days=1),
        axis=1
    )

    # Sort the DataFrame by 'date_from' in ascending order
    df_sorted = df.sort_values(by='date_from', ascending=True)

    # Create Gantt Chart with the sorted data and reverse the y-axis order to reflect the desired task ordering
    fig = px.timeline(df_sorted, x_start="date_from", x_end="date_to", y="name", title="Project Gantt Chart")
    
    # Update y-axis to reflect the task order based on the sorted DataFrame in ascending order
    fig.update_yaxes(categoryorder='array', categoryarray=df_sorted['name'].tolist()[::-1])  # Reverse the list
    
    fig.update_layout(xaxis_title="Date", yaxis_title="Tasks")

    # Create a simple HTML representation of the tasks
    task_list = df_sorted.apply(lambda row: html.Div(f"{row['name']} ({row['date_from'].date()} - {row['date_to'].date()})", style={'margin-bottom': '5px', 'font-size': '18px', 'max-width': '800px', 'word-wrap': 'break-word'}), axis=1)
    calendar_div = html.Div(list(task_list), style={'padding': '10px', 'font-size': '18px'})  # Updated to ensure text is more spread out

    # Create a calendar representation with a large format allowing task addition
    current_year = datetime.now().year
    months_dropdown = dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': calendar.month_name[i], 'value': i} for i in range(1, 13)],
        value=datetime.now().month,
        clearable=False,
        style={'width': '300px', 'margin-bottom': '20px'}
    )

    # Generate the current month's calendar in a large format
    cal = calendar.HTMLCalendar().formatmonth(current_year, datetime.now().month)
    calendar_html = html.Div([
        months_dropdown,
        html.Div(id='calendar-task-container', children=[
            html.Iframe(id='calendar-iframe', srcDoc=cal, style={'border': '0', 'width': '100%', 'height': '400px'})
        ], style={'width': '100%', 'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '10px', 'background-color': '#f9f9f9'})
    ])

    return fig, calendar_div, calendar_html

# Callback to update the calendar when the month dropdown changes
@dash_app.callback(
    Output('calendar-iframe', 'srcDoc'),
    Input('month-dropdown', 'value')
)
def update_calendar(month):
    current_year = datetime.now().year
    cal = calendar.HTMLCalendar().formatmonth(current_year, month)
    return cal

@app.route('/templates/index.html')
def home():
    return render_template('index.html')

@app.route('/templates/charter.html')
def dashboard():
    return render_template('charter.html', data=dashboard_data)

@app.route('/templates/milestones.html')
def milestones():
    return render_template('milestones.html')

@app.route('/templates/budget.html')
def budget():
    return render_template('budget.html')

@app.route('/templates/wbs.html')
def wbs():
    return render_template('wbs.html')

@app.route('/templates/aoa.html')
def aoa():
    return render_template('aoa.html')

@app.route('/templates/sow.html')
def sow():
    return render_template('sow.html')

@app.route('/templates/team.html')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(debug=True)
