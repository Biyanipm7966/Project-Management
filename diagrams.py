import matplotlib.pyplot as plt
import os

def create_gantt_chart():
    # Placeholder for Gantt chart creation
    tasks = ['Kickoff', 'Development', 'Testing', 'Finalization', 'Release']
    start_dates = [1, 3, 5, 7, 9]
    durations = [2, 4, 3, 2, 1]

    fig, ax = plt.subplots()
    ax.barh(tasks, durations, left=start_dates)

    plt.xlabel('Timeline (Months)')
    plt.title('Project Gantt Chart')

    gantt_chart_path = os.path.join('static', 'gantt_chart.png')
    plt.savefig(gantt_chart_path)
    return gantt_chart_path

def create_wbs_diagram():
    # Placeholder for WBS diagram creation
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'WBS Diagram Placeholder', fontsize=12, ha='center')

    wbs_diagram_path = os.path.join('static', 'wbs_diagram.png')
    plt.savefig(wbs_diagram_path)
    return wbs_diagram_path

def create_aoa_diagram():
    # Placeholder for AOA diagram creation
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, 'AOA Diagram Placeholder', fontsize=12, ha='center')

    aoa_diagram_path = os.path.join('static', 'aoa_diagram.png')
    plt.savefig(aoa_diagram_path)
    return aoa_diagram_path
