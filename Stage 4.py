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
                for task_data in data:
                    self.tasks.append(Task(**task_data))
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Error: Invalid JSON file.")

    def get_filtered_tasks(self, name_filter=None, priority_filter=None, due_date_filter=None):
        filtered = []
        for task in self.tasks:
            if name_filter and name_filter.lower() not in task.name.lower():
                continue
            if priority_filter and task.priority != priority_filter:
                continue
            if due_date_filter and task.due_date != due_date_filter:
                continue
            filtered.append(task)
        return filtered

    def sort_tasks(self, sort_key='name'):
        if sort_key == 'name':
            self.tasks.sort(key=self._get_name)
        elif sort_key == 'priority':
            self.tasks.sort(key=self._get_priority_value)
        elif sort_key == 'due_date':
            self.tasks.sort(key=self._get_due_date)

    # Helper methods to replace lambda
    def _get_name(self, task):
        return task.name.lower()

    def _get_priority_value(self, task):
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        return priority_order.get(task.priority, 4)

    def _get_due_date(self, task):
        return datetime.strptime(task.due_date, "%Y-%m-%d")


class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Task Manager")
        self.task_manager = TaskManager()
        self.setup_gui()
        self.populate_tree()

    def setup_gui(self):
        # Filter section
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Name:").grid(row=0, column=0)
        self.name_filter = tk.Entry(filter_frame)
        self.name_filter.grid(row=0, column=1)

        tk.Label(filter_frame, text="Priority:").grid(row=0, column=2)
        self.priority_filter = ttk.Combobox(filter_frame, values=["", "High", "Medium", "Low"])
        self.priority_filter.grid(row=0, column=3)

        tk.Label(filter_frame, text="Due Date:").grid(row=0, column=4)
        self.due_date_filter = tk.Entry(filter_frame)
        self.due_date_filter.grid(row=0, column=5)

        filter_button = tk.Button(filter_frame, text="Filter", command=self.apply_filter)
        filter_button.grid(row=0, column=6, padx=5)

        # Treeview setup
        self.tree = ttk.Treeview(self.root, columns=("name", "description", "priority", "due_date"), show='headings')
        self.tree.heading("name", text="Name", command=self.sort_by_name)
        self.tree.heading("priority", text="Priority", command=self.sort_by_priority)
        self.tree.heading("due_date", text="Due Date", command=self.sort_by_due_date)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def populate_tree(self, tasks=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        tasks = tasks or self.task_manager.tasks
        for task in tasks:
            self.tree.insert('', 'end', values=(task.name, task.description, task.priority, task.due_date))

    def apply_filter(self):
        filtered = self.task_manager.get_filtered_tasks(
            name_filter=self.name_filter.get().strip(),
            priority_filter=self.priority_filter.get(),
            due_date_filter=self.due_date_filter.get().strip()
        )
        self.populate_tree(filtered)

    # Simplified sorting methods
    def sort_by_name(self):
        self.task_manager.sort_tasks('name')
        self.populate_tree()

    def sort_by_priority(self):
        self.task_manager.sort_tasks('priority')
        self.populate_tree()

    def sort_by_due_date(self):
        self.task_manager.sort_tasks('due_date')
        self.populate_tree()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()