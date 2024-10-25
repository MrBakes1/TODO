import customtkinter as ctk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x400")

        # Initialize task list
        self.tasks = []

        # Create the main frame
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create a textbox to display tasks
        self.task_textbox = ctk.CTkTextbox(self.frame, width=400, height=200)
        self.task_textbox.pack(pady=10)

        # Create an entry box to add new tasks
        self.task_entry = ctk.CTkEntry(self.root, width=40)
        self.task_entry.pack(pady=10)

        # Create buttons
        self.add_task_button = ctk.CTkButton(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.remove_task_button = ctk.CTkButton(self.root, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(pady=5)

        # Button to switch color scheme
        self.toggle_theme_button = ctk.CTkButton(self.root, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.pack(pady=5)

        # Initial appearance settings
        self.appearance_mode = "dark"
        self.color_theme = "blue"

    def toggle_theme(self):
        """Toggle between dark and light mode, and switch color themes."""
        if self.appearance_mode == "dark":
            self.appearance_mode = "light"
            self.color_theme = "green"
        else:
            self.appearance_mode = "dark"
            self.color_theme = "blue"

        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme(self.color_theme)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, ctk.END)  # Clear the entry box
        else:
            ctk.CTkMessageBox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        task = self.task_entry.get()
        if task in self.tasks:
            self.tasks.remove(task)  # Remove from task list
            self.update_task_list()  # Update textbox display
            self.task_entry.delete(0, ctk.END)  # Clear the entry box
        else:
            ctk.CTkMessageBox.showwarning("Warning", "Task not found.")

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
