import json
from datetime import datetime

# List to store tasks, each task is a dictionary now
tasks = []


# Functions for CRUD operations
def add_task():
    name = input("\nEnter task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    # Check for duplicates
    for task in tasks:
        if task["name"].lower() == name.lower():
            print("Task already exists. Try updating it instead.")
            return

    description = input("Enter task description: ").strip()

    # Ensure priority is valid
    valid_priorities = {"High", "Medium", "Low"}
    while True:
        priority = input("Enter priority (High, Medium, Low): ").strip().capitalize()
        if priority in valid_priorities:
            break
        print("Invalid priority! Please enter 'High', 'Medium', or 'Low'.")

    # Valid date format
    while True:
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please enter the due date in YYYY-MM-DD format.")

    # Create and add the new task
    new_task = {
        "name": name,
        "description": description,
        "priority": priority,
        "due_date": due_date
    }
    tasks.append(new_task)
    print(f"Task '{name}' added successfully!")

# Display tasks in readable format
def view_tasks():
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nCurrent Tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['name']} | {task['description']} (Priority: {task['priority']}, Due: {task['due_date']})")

# Update an existing task's fields
def update_task():
    name = input("\nEnter the name of the task to update: ").strip()

    for task in tasks:
        if task["name"] == name:
            print("Leave blank to keep the existing value.")

            # Update an existing task's fields
            new_description = input("Enter new description: ").strip()
            if new_description:
                task["description"] = new_description

            # Update priority with validation
            valid_priorities = {"High", "Medium", "Low"}
            while True:
                new_priority = input("Enter new priority (High, Medium, Low): ").strip().capitalize()
                if not new_priority:
                    break
                if new_priority in valid_priorities:
                    task["priority"] = new_priority
                    break
                print("Invalid priority! Please enter 'High', 'Medium', or 'Low'.")

            # Update due date with validation
            while True:
                new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                if not new_due_date:
                    break
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    task["due_date"] = new_due_date
                    break
                except ValueError:
                    print("Invalid date format! Please enter the due date in YYYY-MM-DD format.")

            print(f"Task '{name}' updated successfully!")
            return

    print("Task not found.")

# Delete a task by its name
def delete_task():
    name = input("\nEnter the name of the task to delete: ").strip()

    for i, task in enumerate(tasks):
        if task["name"] == name:
            tasks.pop(i)
            print(f"Task '{name}' deleted successfully!")
            return

    print("Task not found.")


# JSON file handling functions

# Load tasks from JSON file
def load_tasks_from_json():
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                for item in data:
                    # Ensure each loaded item has all necessary keys
                    if all(k in item for k in ("name", "description", "priority", "due_date")):
                        tasks.append(item)
                    else:
                        print("Skipping malformed task data.")
            print("Tasks loaded successfully!")
    except FileNotFoundError:
        print("No saved tasks found. Starting newly.")
    except json.JSONDecodeError:
        print("Could not parse JSON. Starting with an empty task list.")
    except Exception as e:
        print(f"Oops, something went wrong while loading tasks: {e}")

# Save tasks to a JSON file before program exits
def save_tasks_to_json():
    try:
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)
        print("All tasks have been saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")

# Main Menu Loop

# Only runs when the script is executed directly
if __name__ == "__main__":
    load_tasks_from_json()  # Load saved tasks when program starts
    while True:
        print("\nTask Manager")
        print("==============")
        print("1. Add task")
        print("2. View tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Save and Exit")
        print("==============")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            update_task()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            save_tasks_to_json()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")
