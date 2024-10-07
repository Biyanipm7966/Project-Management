import matplotlib.pyplot as plt
import os

def create_gantt_chart():
    # Simple example of a Gantt chart
    tasks = ['Kickoff', 'Development', 'Testing', 'Finalization', 'Release']
    start_dates = [1, 3, 5, 7, 9]
    durations = [2, 4, 3, 2, 1]

    fig, ax = plt.subplots()
    ax.barh(tasks, durations, left=start_dates)

    plt.xlabel('Timeline (Months)')
    plt.title('Project Gantt Chart')

    # Save the chart as a static file
    gantt_chart_path = os.path.join('static', 'gantt_chart.png')
    plt.savefig(gantt_chart_path)

    return gantt_chart_path
