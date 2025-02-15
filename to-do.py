import mysql.connector
import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List with MySQL")
        
        # Connect to MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",      # Change this if you use a different username
            password="",      # Enter your MySQL root password here
            database="todo_db"
        )
        self.cursor = self.conn.cursor()

        # Create task input
        self.task_label = tk.Label(root, text="Enter Task:")
        self.task_label.pack()
        
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack()
        
        # Buttons
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.listbox = tk.Listbox(root, height=10, width=50)
        self.listbox.pack()
        
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        # Load existing tasks from the database
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def load_tasks(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM tasks")
        tasks = self.cursor.fetchall()
        for task in tasks:
            self.listbox.insert(tk.END, f"{task[0]}. {task[1]}")

    def delete_task(self):
        selected_task = self.listbox.curselection()
        if selected_task:
            task_id = self.listbox.get(selected_task).split(".")[0]
            self.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.conn.commit()
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "No task selected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
