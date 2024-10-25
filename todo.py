import customtkinter as ctk
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x400")

        self.tasks = []
        self.load_tasks()

        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.task_textbox = ctk.CTkTextbox(self.frame, width=400, height=200)
        self.task_textbox.pack(pady=10)

        self.update_task_list()

        self.task_entry = ctk.CTkEntry(self.root, width=40)
        self.task_entry.pack(pady=10)

        self.add_task_button = ctk.CTkButton(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.remove_task_button = ctk.CTkButton(self.root, text="Remove Task", command=self.remove_task)
        self.remove_task_button.pack(pady=5)

        self.toggle_theme_button = ctk.CTkButton(self.root, text="Toggle Mode", command=self.toggle_theme)
        self.toggle_theme_button.pack(pady=5)

        self.change_color_button = ctk.CTkButton(self.root, text="Change Color Theme", command=self.change_color_theme)
        self.change_color_button.pack(pady=5)

        self.appearance_mode = "dark"
        self.color_themes = ["blue", "green"]
        self.current_color_theme_index = 0

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

    def change_color_theme(self):
        """Change the color theme to the next one in the list."""
        self.current_color_theme_index = (self.current_color_theme_index + 1) % len(self.color_themes)
        new_color_theme = self.color_themes[self.current_color_theme_index]
        ctk.set_default_color_theme(new_color_theme)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.save_tasks()
            self.task_entry.delete(0, ctk.END)
        else:
            ctk.CTkMessageBox.showwarning("Warning", "Please enter a task.")

    def remove_task(self):
        try:
            selected_task = self.task_textbox.get("1.0", ctk.END).strip().split("\n")
            if selected_task:
                task_to_remove = selected_task[-1]
                if task_to_remove in self.tasks:
                    self.tasks.remove(task_to_remove)
                    self.update_task_list()
                    self.save_tasks()
        except IndexError:
            ctk.CTkMessageBox.showwarning("Warning", "Please select a task to remove.")

    def update_task_list(self):
        self.task_textbox.delete("1.0", ctk.END)
        for task in self.tasks:
            self.task_textbox.insert(ctk.END, f"{task}\n")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()
