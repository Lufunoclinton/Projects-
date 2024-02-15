import json
import datetime
import tkinter as tk
from tkinter import messagebox

PROJECTS_FILE = "projects.json"

def load_projects():
    try:
        with open(PROJECTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as file:
        json.dump(projects, file, indent=4)

def create_project(name, description):
    projects = load_projects()
    project_id = len(projects) + 1
    projects.append({"ID": project_id, "Name": name, "Description": description, "Tasks": []})
    save_projects(projects)
    messagebox.showinfo("Success", "Project created successfully.")

def assign_task(project_id, task_name, due_date, priority, team_members):
    projects = load_projects()
    project = next((p for p in projects if p["ID"] == project_id), None)
    if project:
        task_id = len(project["Tasks"]) + 1
        project["Tasks"].append({
            "ID": task_id,
            "Name": task_name,
            "Due Date": due_date,
            "Priority": priority,
            "Team Members": team_members,
            "Status": "Pending"
        })
        save_projects(projects)
        messagebox.showinfo("Success", "Task assigned successfully.")
    else:
        messagebox.showerror("Error", "Invalid project ID.")

def track_deadlines():
    projects = load_projects()
    current_date = datetime.date.today()
    deadlines = []
    for project in projects:
        for task in project["Tasks"]:
            due_date = datetime.datetime.strptime(task["Due Date"], "%Y-%m-%d").date()
            days_remaining = (due_date - current_date).days
            deadlines.append((project["Name"], task["Name"], due_date, days_remaining))
    sorted_deadlines = sorted(deadlines, key=lambda x: x[2])  # Sort by due date
    messagebox.showinfo("Deadlines", "\n".join(f"{proj}: {task} - Due Date: {date} - Days Remaining: {days}" for proj, task, date, days in sorted_deadlines))

class ProjectManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Management System")
        self.root.geometry("400x300")

        self.create_project_frame = tk.Frame(self.root)
        self.create_project_frame.pack(pady=10)

        tk.Label(self.create_project_frame, text="Project Name:").grid(row=0, column=0)
        self.project_name_entry = tk.Entry(self.create_project_frame)
        self.project_name_entry.grid(row=0, column=1)

        tk.Label(self.create_project_frame, text="Description:").grid(row=1, column=0)
        self.description_entry = tk.Entry(self.create_project_frame)
        self.description_entry.grid(row=1, column=1)

        tk.Button(self.create_project_frame, text="Create Project", command=self.create_project).grid(row=2, columnspan=2)

        self.assign_task_frame = tk.Frame(self.root)
        self.assign_task_frame.pack(pady=10)

        tk.Label(self.assign_task_frame, text="Project ID:").grid(row=0, column=0)
        self.project_id_entry = tk.Entry(self.assign_task_frame)
        self.project_id_entry.grid(row=0, column=1)

        tk.Label(self.assign_task_frame, text="Task Name:").grid(row=1, column=0)
        self.task_name_entry = tk.Entry(self.assign_task_frame)
        self.task_name_entry.grid(row=1, column=1)

        tk.Label(self.assign_task_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        self.due_date_entry = tk.Entry(self.assign_task_frame)
        self.due_date_entry.grid(row=2, column=1)

        tk.Label(self.assign_task_frame, text="Priority:").grid(row=3, column=0)
        self.priority_entry = tk.Entry(self.assign_task_frame)
        self.priority_entry.grid(row=3, column=1)

        tk.Label(self.assign_task_frame, text="Team Members:").grid(row=4, column=0)
        self.team_members_entry = tk.Entry(self.assign_task_frame)
        self.team_members_entry.grid(row=4, column=1)

        tk.Button(self.assign_task_frame, text="Assign Task", command=self.assign_task).grid(row=5, columnspan=2)

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(pady=10)

        tk.Button(self.menu_frame, text="Track Deadlines", command=self.track_deadlines).grid(row=0, column=0)

    def create_project(self):
        name = self.project_name_entry.get()
        description = self.description_entry.get()
        if name and description:
            create_project(name, description)
        else:
            messagebox.showerror("Error", "Please enter project name and description.")

    def assign_task(self):
        project_id = self.project_id_entry.get()
        task_name = self.task_name_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()
        team_members = self.team_members_entry.get()
        if project_id and task_name and due_date and priority and team_members:
            assign_task(int(project_id), task_name, due_date, priority, team_members)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def track_deadlines(self):
        track_deadlines()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagementGUI(root)
    root.mainloop()
