import datetime
import os
from PIL import Image
import tkinter



projects = []


class ScrollableCheckBoxFrame(tkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = tkinter.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10))
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class ScrollableRadiobuttonFrame(tkinter.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.radiobutton_variable = tkinter.StringVar()
        self.radiobutton_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        radiobutton = tkinter.CTkRadioButton(self, text=item, value=item, variable=self.radiobutton_variable)
        if self.command is not None:
            radiobutton.configure(command=self.command)
        radiobutton.grid(row=len(self.radiobutton_list), column=0, pady=(0, 10))
        self.radiobutton_list.append(radiobutton)

    def remove_item(self, item):
        for radiobutton in self.radiobutton_list:
            if item == radiobutton.cget("text"):
                radiobutton.destroy()
                self.radiobutton_list.remove(radiobutton)
                return

    def get_checked_item(self):
        return self.radiobutton_variable.get()


class ScrollableLabelButtonFrame(tkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = tkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label =tkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = tkinter.CTkButton(self, text="Command", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return


class App(tkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Project Management System")
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.create_widgets()

    def create_widgets(self):
        # create scrollable checkbox frame
        self.scrollable_checkbox_frame = ScrollableCheckBoxFrame(master=self, width=200, command=self.checkbox_frame_event,
                                                                 item_list=["Project 1", "Project 2", "Project 3"])
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")
        self.scrollable_checkbox_frame.add_item("New Project")

        # create scrollable radiobutton frame
        self.scrollable_radiobutton_frame = ScrollableRadiobuttonFrame(master=self, width=500, command=self.radiobutton_frame_event,
                                                                       item_list=["Task 1", "Task 2", "Task 3"],
                                                                       label_text="Task List")
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=15, pady=15, sticky="ns")
        self.scrollable_radiobutton_frame.configure(width=200)
        self.scrollable_radiobutton_frame.remove_item("Task 3")

        # create scrollable label and button frame
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=300, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nsew")
        for i in range(20):  # add items with images
            self.scrollable_label_button_frame.add_item(f"Image and Item {i}", image=tkinter.CTkImage(Image.open(os.path.join(current_dir, "test_images", "chat_light.png"))))

    def checkbox_frame_event(self):
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")

    def label_button_frame_event(self, item):
        print(f"label button frame clicked: {item}")


def create_project():
    project_name = input("Enter the project name: ")
    project_description = input("Enter the project description: ")
    projects.append({"Name": project_name, "Description": project_description, "Tasks": []})
    print("Project created successfully.")


def assign_task_to_project():
    project_name = input("Enter the project name to which the task belongs: ")
    project = next((p for p in projects if p["Name"] == project_name), None)
    if project:
        task = input("Enter a new task: ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")
        priority = input("Enter the priority (high, medium, low): ").lower()
        project["Tasks"].append({"Task": task, "Due Date": due_date, "Done": False, "Priority": priority})
        print("Task assigned successfully.")
    else:
        print("Project not found.")


def main():
    while True:
        print('\n===== Project Management System =====')
        print("1. Create Project")
        print("2. Assign Task to Project")
        print("3. Set Task Dependency")
        print("4. Track Deadlines")
        print("5. View Project")
        print("6. Progress Monitoring")
        print("7. Quit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            create_project()
        elif choice == 2:
            assign_task_to_project()
        elif choice == 3:
            pass  # Placeholder for set_task_dependency function
        elif choice == 4:
            pass  # Placeholder for track_deadline function
        elif choice == 5:
            pass  # Placeholder for view_project function
        elif choice == 6:
            pass  # Placeholder for progress_monitoring function
        elif choice == 7:
            print("Thank you for using the Project Management System.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    tkinter.set_appearance_mode("dark")
    app = App()
    app.mainloop()
