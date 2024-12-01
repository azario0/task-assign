import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to add teacher
def add_teacher():
    teacher_name = entry_teacher.get()
    if teacher_name:
        teachers_list.append(teacher_name)
        list_teachers.insert(parent='', index='end', iid=None, text=teacher_name)
        entry_teacher.delete(0, "end")
        update_comboboxes()
        save_teachers_to_csv()  # Save teachers after addition
    else:
        messagebox.showwarning("Warning", "Please enter a teacher name.")

# Function to save teachers to CSV
def save_teachers_to_csv():
    df = pd.DataFrame(teachers_list, columns=['Teacher'])
    df.to_csv('teachers.csv', index=False)

# Function to load teachers from CSV
def load_teachers_from_csv():
    try:
        df = pd.read_csv('teachers.csv')
        global teachers_list
        teachers_list = df['Teacher'].tolist()
        for teacher in teachers_list:
            list_teachers.insert(parent='', index='end', iid=None, text=teacher)
        update_comboboxes()
    except FileNotFoundError:
        # If the file doesn't exist, do nothing
        pass

# Function to load tasks from CSV
def load_tasks_from_csv():
    try:
        df = pd.read_csv('tasks.csv')
        global tasks_list
        tasks_list = df.to_dict(orient='records')
        # Update any UI elements that display tasks
    except FileNotFoundError:
        # If the file doesn't exist, do nothing
        pass

# Function to update combo boxes
def update_comboboxes():
    combo_teacher['values'] = teachers_list
    combo_teacher_comp['values'] = teachers_list
    combo_teacher_chart['values'] = teachers_list

# Function to assign task
def assign_task():
    teacher = combo_teacher.get()
    date = cal.get_date()
    task = entry_task.get()
    if teacher and task:
        tasks_list.append({'Teacher': teacher, 'Date': date, 'Task': task, 'Status': 'Pending'})
        entry_task.delete(0, "end")
        save_to_csv()  # Save tasks after assignment
        update_task_list()
    else:
        messagebox.showwarning("Warning", "Please select a teacher and enter a task.")

# Function to mark task as complete
def mark_complete():
    selected_iid = list_tasks.selection()
    if selected_iid:
        item = list_tasks.item(selected_iid)
        task_details = item['values']
        for task in tasks_list:
            if task['Teacher'] == combo_teacher_comp.get() and task['Date'] == task_details[0] and task['Task'] == task_details[1]:
                task['Status'] = 'Completed'
                break
        update_task_list()
        save_to_csv()  # Save tasks after completion
    else:
        messagebox.showwarning("Warning", "Please select a task to mark as complete.")

# Function to generate chart
def generate_chart(event=None):
    selected_teacher = combo_teacher_chart.get()
    completed = 0
    pending = 0
    for task in tasks_list:
        if task['Teacher'] == selected_teacher:
            if task['Status'] == 'Completed':
                completed += 1
            else:
                pending += 1
    fig.clear()
    ax = fig.add_subplot(111)
    if completed + pending > 0:
        ax.pie([completed, pending], labels=['Completed', 'Pending'], autopct='%1.1f%%')
    else:
        ax.text(0.5, 0.5, 'No tasks to display', ha='center', va='center')
    ax.set_title(f"Task Status for {selected_teacher}")
    canvas.draw()

# Function to save tasks to CSV
def save_to_csv():
    df = pd.DataFrame(tasks_list)
    df.to_csv('tasks.csv', index=False)

def update_task_list():
    selected_teacher = combo_teacher_comp.get()
    list_tasks.delete(*list_tasks.get_children())
    for task in tasks_list:
        if task['Teacher'] == selected_teacher:
            list_tasks.insert(parent='', index='end', iid=None, values=(task['Date'], task['Task'], task['Status']))

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Initialize the main window
app = ctk.CTk()
app.title("Teacher Task Management App")
app.geometry("800x600")

# Create a Notebook (Tabs) widget
notebook = ttk.Notebook(app)
notebook.pack(pady=10, expand=True, fill="both")

# Lists to store teachers and tasks
teachers_list = []
tasks_list = []

# Teachers Tab
teachers_tab = ctk.CTkFrame(notebook)
notebook.add(teachers_tab, text="Teachers")

# Frame for teacher input
frame_teachers = ctk.CTkFrame(teachers_tab)
frame_teachers.pack(pady=20)

label_teacher = ctk.CTkLabel(frame_teachers, text="Enter Teacher Name:")
label_teacher.grid(row=0, column=0, padx=10, pady=10)

entry_teacher = ctk.CTkEntry(frame_teachers, width=200)
entry_teacher.grid(row=0, column=1, padx=10, pady=10)

button_add_teacher = ctk.CTkButton(frame_teachers, text="Add Teacher", command=add_teacher)
button_add_teacher.grid(row=0, column=2, padx=10, pady=10)

# Treeview to display teachers
list_teachers = ttk.Treeview(teachers_tab, height=10, show='tree')
list_teachers.pack(pady=20)

# Assign Tasks Tab
assign_tab = ctk.CTkFrame(notebook)
notebook.add(assign_tab, text="Assign Tasks")

# Frame for task assignment
frame_assign = ctk.CTkFrame(assign_tab)
frame_assign.pack(pady=20)

label_select_teacher = ctk.CTkLabel(frame_assign, text="Select Teacher:")
label_select_teacher.grid(row=0, column=0, padx=10, pady=10)

# Combobox for selecting teacher
combo_teacher = ttk.Combobox(frame_assign, values=teachers_list)
combo_teacher.grid(row=0, column=1, padx=10, pady=10)

# Calendar for selecting day
cal = Calendar(frame_assign, selectmode='day')
cal.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

label_task = ctk.CTkLabel(frame_assign, text="Enter Task:")
label_task.grid(row=2, column=0, padx=10, pady=10)

entry_task = ctk.CTkEntry(frame_assign, width=200)
entry_task.grid(row=2, column=1, padx=10, pady=10)

button_assign = ctk.CTkButton(frame_assign, text="Assign Task", command=assign_task)
button_assign.grid(row=3, column=1, padx=10, pady=10)

# Task Completion Tab
completion_tab = ctk.CTkFrame(notebook)
notebook.add(completion_tab, text="Task Completion")

# Frame for task completion
frame_completion = ctk.CTkFrame(completion_tab)
frame_completion.pack(pady=20)

label_select_teacher_comp = ctk.CTkLabel(frame_completion, text="Select Teacher:")
label_select_teacher_comp.grid(row=0, column=0, padx=10, pady=10)

combo_teacher_comp = ttk.Combobox(frame_completion, values=teachers_list)
combo_teacher_comp.grid(row=0, column=1, padx=10, pady=10)

# Treeview to display tasks
list_tasks = ttk.Treeview(frame_completion, height=10, show='headings', columns=('Date', 'Task', 'Status'))
list_tasks.heading('Date', text='Date')
list_tasks.heading('Task', text='Task')
list_tasks.heading('Status', text='Status')
list_tasks.column('Date', width=100)
list_tasks.column('Task', width=200)
list_tasks.column('Status', width=100)
list_tasks.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

combo_teacher_comp.bind("<<ComboboxSelected>>", lambda event: update_task_list())

button_mark_complete = ctk.CTkButton(frame_completion, text="Mark as Complete", command=mark_complete)
button_mark_complete.grid(row=2, column=1, padx=10, pady=10)

# Charts Tab
charts_tab = ctk.CTkFrame(notebook)
notebook.add(charts_tab, text="Charts")

# Frame for charts
frame_charts = ctk.CTkFrame(charts_tab)
frame_charts.pack(pady=20)

label_select_teacher_chart = ctk.CTkLabel(frame_charts, text="Select Teacher:")
label_select_teacher_chart.grid(row=0, column=0, padx=10, pady=10)

combo_teacher_chart = ttk.Combobox(frame_charts, values=teachers_list)
combo_teacher_chart.grid(row=0, column=1, padx=10, pady=10)

# Figure and Canvas for chart
fig = plt.Figure(figsize=(5,4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_charts)
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10)

combo_teacher_chart.bind("<<ComboboxSelected>>", generate_chart)

# Load teachers and tasks on startup
load_teachers_from_csv()
load_tasks_from_csv()

# Run the app
app.mainloop()