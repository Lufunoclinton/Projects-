import datetime

projects = []


def create_project():
    project_id = input("Enter a unique project identifier: ")
    project_name = input("Enter the project name: ")
    project_description = input("Enter the project description: ")
    projects.append({"ID": project_id, "Name": project_name, "Description": project_description, "Tasks": []})
    print("Project created successfully.")


def assign_task_to_project():
    project_id = input("Enter the project ID to which the task belongs: ")
    project = next((p for p in projects if p["ID"] == project_id), None)
    if project:
        task = input("Enter a new task: ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")
        priority = input("Enter the priority (high, medium, low): ").lower()
        project["Tasks"].append({"Task": task, "Due Date": due_date, "Done": False, "Priority": priority})
        print("Task assigned successfully.")
    else:
        print("Invalid project ID.")


def set_task_dependency():
    project_id = input("Enter the project ID: ")
    project = next((p for p in projects if p["ID"] == project_id), None)
    if project:
        task_index = int(input("Enter the task number to set dependency: ")) - 1
        dependency_index = int(input("Enter the dependent task number: ")) - 1
        if 0 <= task_index < len(project["Tasks"]) and 0 <= dependency_index < len(project["Tasks"]):
            project["Tasks"][task_index].setdefault("Dependencies", []).append(dependency_index)
            print("Dependency set successfully.")
        else:
            print("Invalid task or dependency index.")
    else:
        print("Invalid project ID.")


def track_deadline():
    current_date = datetime.date.today()
    for project in projects:
        print(f"\nProject: {project['Name']} - {project['Description']}")
        for i, task in enumerate(project["Tasks"], start=1):
            due_date = datetime.datetime.strptime(task["Due Date"], "%Y-%m-%d").date()
            days_remaining = (due_date - current_date).days
            print(f'Task {i}: {task["Task"]} - Due Date: {task["Due Date"]} - Days Remaining: {days_remaining}')


def view_project():
    project_id = input("Enter the project ID to view tasks: ")
    project = next((p for p in projects if p["ID"] == project_id), None)
    if project:
        print(f"\nProject: {project['Name']} - {project['Description']}")
        for i, task in enumerate(project["Tasks"], start=1):
            status = "Done" if task["Done"] else "Not Done"
            print(f'Task {i}: {task["Task"]} - Due Date: {task["Due Date"]} - {status}')
    else:
        print("Invalid project ID.")


def progress_monitoring():
    project_id = input("Enter the project ID to monitor progress: ")
    project = next((p for p in projects if p["ID"] == project_id), None)
    if project:
        track_progress(project)
    else:
        print("Invalid project ID.")


def track_progress(project):
    total_tasks = len(project["Tasks"])
    completed_tasks = sum(task["Done"] for task in project["Tasks"])
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    print(f"\nProject: {project['Name']} - {project['Description']}")
    print(f"Total Tasks: {total_tasks}, Completed: {completed_tasks}, Progress: {progress_percentage:.2f}%.")


def main():
    while True:
        print('\n===== Project Management System =====')
        print("1. Create Project")
        print("2. Assign Task to Project")
        print("3. Set Task Dependency")
        print("4. Track Deadlines")
        print("5. Team Collaboration")
        print("6. Progress Monitoring")
        print("7. Quit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_project()
        elif choice == 2:
            assign_task_to_project()
        elif choice == 3:
            set_task_dependency()
        elif choice == 4:
            track_deadline()
        elif choice == 5:
            view_project()
        elif choice == 6:
            progress_monitoring()
        elif choice == 7:
            print("Thank you for using the Project Management System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()