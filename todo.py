import customtkinter as ctk
from tkcalendar import Calendar 
import os
from datetime import datetime
from tkinter import messagebox 

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x800")

        self.tasks = []
        self.due_dates = []
        self.load_tasks()

        # Create the main frame
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a textbox to display tasks
        self.task_textbox = ctk.CTkTextbox(self.frame, width=400, height=200)
        self.task_textbox.pack(pady=10)
        self.task_textbox.bind("<Double-1>", self.select_task_to_edit)

        self.update_task_list()

        self.task_entry = ctk.CTkEntry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.due_date_picker = Calendar(self.root, selectmode='day')
        self.due_date_picker.pack(pady=10)

        self.add_task_button = ctk.CTkButton(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.remove_task_button = ctk.CTkButton(self.root, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(pady=5)

        self.toggle_theme_button = ctk.CTkButton(self.root, text="Toggle Mode", command=self.toggle_theme)
        self.toggle_theme_button.pack(pady=5)

        self.edit_task_entry = ctk.CTkEntry(self.root, width=40)
        self.edit_task_button = ctk.CTkButton(self.root, text="Save Edit", command=self.save_edited_task)
        
        self.appearance_mode = "dark"
        self.selected_task_index = None

    def load_tasks(self):
        """Load tasks and due dates from a file."""
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                for line in file:
                    task, due_date = line.strip().split(" || ")
                    self.tasks.append(task)
                    self.due_dates.append(due_date)

    def save_tasks(self):
        """Save tasks and due dates to a file."""
        with open("tasks.txt", "w") as file:
            for task, due_date in zip(self.tasks, self.due_dates):
                file.write(f"{task} || {due_date}\n")

    def toggle_theme(self):
        """Toggle between dark and light mode."""
        self.appearance_mode = "light" if self.appearance_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.appearance_mode)

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_picker.get_date()
        if task:
            self.tasks.append(task)
            self.due_dates.append(due_date)
            self.update_task_list()
            self.save_tasks()
            self.task_entry.delete(0, ctk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        try:
            selected_task = self.task_textbox.get("1.0", ctk.END).strip().split("\n")
            if selected_task:
                task_to_remove = selected_task[-1].split(" (Due: ")[0]
                if task_to_remove in self.tasks:
                    index = self.tasks.index(task_to_remove)
                    del self.tasks[index]
                    del self.due_dates[index]
                    self.update_task_list()
                    self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove.")

    def select_task_to_edit(self, event):
        """Handle double-click event to select a task for editing."""
        try:
            line_index = self.task_textbox.index("@%s,%s" % (event.x, event.y)).split(".")[0]
            task_line = self.task_textbox.get(f"{line_index}.0", f"{line_index}.end").strip()

            task, _ = task_line.split(" (Due: ")
            if task in self.tasks:
                self.selected_task_index = self.tasks.index(task)
                self.edit_task_entry.delete(0, ctk.END)
                self.edit_task_entry.insert(0, task)
                self.edit_task_entry.pack(pady=5)
                self.edit_task_button.pack(pady=5)
        except IndexError:
            messagebox.showwarning("Warning", "Please double-click on a valid task.")

    def save_edited_task(self):
        """Save the edited task."""
        if self.selected_task_index is not None:
            edited_task = self.edit_task_entry.get()
            if edited_task:
                self.tasks[self.selected_task_index] = edited_task
                self.update_task_list()
                self.save_tasks()

                self.edit_task_entry.pack_forget()
                self.edit_task_button.pack_forget()

    def update_task_list(self):
        self.task_textbox.delete("1.0", ctk.END)
        for task, due_date in zip(self.tasks, self.due_dates):
            self.task_textbox.insert(ctk.END, f"{task} (Due: {due_date})\n")

        self.check_due_tasks()

    def check_due_tasks(self):
        """Check if any tasks are due today or overdue, and show reminders."""
        today = datetime.today().date()
        for task, due_date in zip(self.tasks, self.due_dates):
            due_date_obj = datetime.strptime(due_date, "%m/%d/%y").date()
            if due_date_obj <= today:
                messagebox.showinfo("Reminder", f"Task '{task}' is due today or overdue!")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")  # options "green" "blue"
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()
