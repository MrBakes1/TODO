import customtkinter as ctk
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x500")

        # Initialize task list and load from file
        self.tasks = []
        self.load_tasks()  # Load tasks when initializing

        # Create the main frame
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a textbox to display tasks
        self.task_textbox = ctk.CTkTextbox(self.frame, width=400, height=200)
        self.task_textbox.pack(pady=10)
        self.task_textbox.bind("<Double-1>", self.select_task_to_edit)  # Bind double-click to edit

        # Display the loaded tasks
        self.update_task_list()

        # Create an entry box to add new tasks
        self.task_entry = ctk.CTkEntry(self.root, width=40)
        self.task_entry.pack(pady=10)

        # Create buttons
        self.add_task_button = ctk.CTkButton(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.remove_task_button = ctk.CTkButton(self.root, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(pady=5)

        # Button to switch appearance mode
        self.toggle_theme_button = ctk.CTkButton(self.root, text="Toggle Mode", command=self.toggle_theme)
        self.toggle_theme_button.pack(pady=5)

        # Entry box and button for editing tasks
        self.edit_task_entry = ctk.CTkEntry(self.root, width=40)
        self.edit_task_button = ctk.CTkButton(self.root, text="Save Edit", command=self.save_edited_task)
        
        # Initial appearance settings
        self.appearance_mode = "dark"
        self.selected_task_index = None  # Index of the selected task to edit

    def load_tasks(self):
        """Load tasks from a file."""
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]

    def save_tasks(self):
        """Save tasks to a file."""
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def toggle_theme(self):
        """Toggle between dark and light mode."""
        self.appearance_mode = "light" if self.appearance_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.appearance_mode)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.save_tasks()  # Save tasks after adding
            self.task_entry.delete(0, ctk.END)  # Clear the entry box
        else:
            ctk.CTkMessageBox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        try:
            selected_task = self.task_textbox.get("1.0", ctk.END).strip().split("\n")
            if selected_task:
                task_to_remove = selected_task[-1]  # Remove the last task from the display
                if task_to_remove in self.tasks:
                    self.tasks.remove(task_to_remove)  # Remove from task list
                    self.update_task_list()  # Update textbox display
                    self.save_tasks()  # Save tasks after removing
        except IndexError:
            ctk.CTkMessageBox.showwarning("Warning", "Please select a task to remove.")

    def select_task_to_edit(self, event):
        """Handle double-click event to select a task for editing."""
        try:
            # Get line number of clicked task
            line_index = self.task_textbox.index("@%s,%s" % (event.x, event.y)).split(".")[0]
            task = self.task_textbox.get(f"{line_index}.0", f"{line_index}.end").strip()

            if task in self.tasks:
                self.selected_task_index = self.tasks.index(task)
                self.edit_task_entry.delete(0, ctk.END)  # Clear edit entry
                self.edit_task_entry.insert(0, task)  # Fill with selected task text
                self.edit_task_entry.pack(pady=5)
                self.edit_task_button.pack(pady=5)
        except IndexError:
            ctk.CTkMessageBox.showwarning("Warning", "Please double-click on a valid task.")

    def save_edited_task(self):
        """Save the edited task."""
        if self.selected_task_index is not None:
            edited_task = self.edit_task_entry.get()
            if edited_task:
                # Update task in the list and refresh display
                self.tasks[self.selected_task_index] = edited_task
                self.update_task_list()
                self.save_tasks()  # Save tasks after editing

                # Hide the edit entry and button
                self.edit_task_entry.pack_forget()
                self.edit_task_button.pack_forget()

    def update_task_list(self):
        self.task_textbox.delete("1.0", ctk.END)  # Clear the current list
        for task in self.tasks:
            self.task_textbox.insert(ctk.END, f"{task}\n")  # Add each task to the textbox

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Initial appearance mode
    ctk.set_default_color_theme("blue")  # Initial color theme
    root = ctk.CTk()  # Create a CustomTkinter window
    app = TodoApp(root)  # Create the application
    root.mainloop()  # Run the application
