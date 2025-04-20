import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Task:
    def __init__(self, name, description, priority, due_date):
        self.name = name
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date
        }


class TaskManager:
    def __init__(self, json_file='tasks.json'):
        self.json_file = json_file
        self.tasks = []
        self.load_tasks_from_json()

    def load_tasks_from_json(self):
        try:
            with open(self.json_file, 'r') as file:
                data = json.load(file)
                self.tasks = [Task(**task) for task in data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            self.tasks = []

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered = self.tasks
        if name_filter and name_filter.strip():
            filtered = [t for t in filtered if self.does_task_contain_name(t, name_filter)]
        if priority_filter:
            filtered = [t for t in filtered if t.priority == priority_filter]
        if due_date_filter and due_date_filter.strip():
            filtered = [t for t in filtered if t.due_date == due_date_filter]
        return filtered

    def does_task_contain_name(self, task, search_term):
        return search_term.lower() in task.name.lower()

    def sort_tasks(self, sort_key='name'):
        if sort_key == 'name':
            self.tasks.sort(key=self.get_name_for_sorting)
        elif sort_key == 'priority':
            self.tasks.sort(key=self.get_priority_for_sorting)
        elif sort_key == 'due_date':
            self.tasks.sort(key=self.get_date_for_sorting)

    def get_name_for_sorting(self, task):
        return task.name.lower()

    def get_priority_for_sorting(self, task):
        priority_values = {'High': 1, 'Medium': 2, 'Low': 3}
        return priority_values.get(task.priority, 4)

    def get_date_for_sorting(self, task):
        return datetime.strptime(task.due_date, "%Y-%m-%d")


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.task_manager = TaskManager()
        self.setup_gui()
        self.populate_tree()
        self.setup_sort_buttons()

    def setup_sort_buttons(self):
        self.tree.heading("name", text="Name", command=self.sort_by_name)
        self.tree.heading("priority", text="Priority", command=self.sort_by_priority)
        self.tree.heading("due_date", text="Due Date", command=self.sort_by_date)

    def setup_gui(self):
        # Filter section
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Name:").grid(row=0, column=0)
        self.name_filter = tk.Entry(frame)
        self.name_filter.grid(row=0, column=1)

        tk.Label(frame, text="Priority:").grid(row=0, column=2)
        self.priority_filter = ttk.Combobox(frame, values=["", "High", "Medium", "Low"], state="readonly")
        self.priority_filter.grid(row=0, column=3)

        tk.Label(frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=4)
        self.due_date_filter = tk.Entry(frame)
        self.due_date_filter.grid(row=0, column=5)

        tk.Button(frame, text="Filter", command=self.apply_filter).grid(row=0, column=6, padx=5)

        # Treeview for displaying tasks
        self.tree = ttk.Treeview(self.root, columns=("name", "description", "priority", "due_date"), show='headings')
        for col in ("name", "description", "priority", "due_date"):
            self.tree.column(col, width=150)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def populate_tree(self, tasks=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if tasks is None:
            tasks = self.task_manager.tasks
        for task in tasks:
            self.tree.insert('', 'end', values=(task.name, task.description, task.priority, task.due_date))

    def apply_filter(self):
        name = self.name_filter.get().strip() or None
        priority = self.priority_filter.get() or None
        due_date = self.due_date_filter.get().strip() or None
        filtered = self.task_manager.get_filtered_tasks(name, priority, due_date)
        self.populate_tree(filtered)

    def sort_by_name(self):
        self.task_manager.sort_tasks('name')
        self.populate_tree()

    def sort_by_priority(self):
        self.task_manager.sort_tasks('priority')
        self.populate_tree()

    def sort_by_date(self):
        self.task_manager.sort_tasks('due_date')
        self.populate_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()