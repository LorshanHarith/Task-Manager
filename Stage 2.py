from datetime import datetime

#List to store tasks, each task will be stored as a list
tasks = []


#Functions for tasks operations
def add_task():
    #Adds a new task to the list.
    name = input("\nEnter task name: ").strip()
    if not name:
        print("Task name cannot be empty.")
        return

    #Checks if task name already exists
    for task in tasks:
        if task[0].lower() == name.lower():
            print("Task already exists. Try updating it instead.")
            return

    description = input("Enter task description: ").strip()

    #Validates priority input
    valid_priorities = {"High", "Medium", "Low"}
    while True:
        priority = input("Enter priority (High, Medium, Low): ").strip().capitalize()
        if priority in valid_priorities:
            break
        print("Invalid priority! Please enter 'High', 'Medium', or 'Low'.")

    #Validates
    # due date input
    while True:
        due_date = input("Enter due date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format! Please enter the due date in YYYY-MM-DD format.")

    tasks.append([name, description, priority, due_date])
    print(f"Task '{name}' added successfully!")


def view_tasks():
    #Displays all tasks.
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nCurrent Tasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task[0]} | {task[1]} (Priority: {task[2]}, Due: {task[3]})")


def update_task():
    #Updates an existing task.
    name = input("\nEnter the name of the task to update: ").strip()

    for task in tasks:
        if task[0] == name:
            print("Leave blank to keep the existing value.")

            new_description = input("Enter new description: ").strip()
            if new_description:
                task[1] = new_description

            valid_priorities = {"High", "Medium", "Low"}
            while True:
                new_priority = input("Enter new priority (High, Medium, Low): ").strip().capitalize()
                if not new_priority:
                    break
                if new_priority in valid_priorities:
                    task[2] = new_priority
                    break
                print("Invalid priority! Please enter 'High', 'Medium', or 'Low'.")

            while True:
                new_due_date = input("Enter new due date (YYYY-MM-DD): ").strip()
                if not new_due_date:
                    break
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    task[3] = new_due_date
                    break
                except ValueError:
                    print("Invalid date format! Please enter the due date in YYYY-MM-DD format.")

            print(f"Task '{name}' updated successfully!")
            return

    print("Task not found.")


def delete_task():
    #Deletes a task from the list.
    name = input("\nEnter the name of the task to delete: ").strip()

    for i, task in enumerate(tasks):
        if task[0] == name:
            tasks.pop(i)
            print(f"Task '{name}' deleted successfully!")
            return

    print("Task not found.")


def load_tasks_from_file():
    #Loads tasks from a file
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                try:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        name, description, priority, due_date = parts
                        tasks.append([name, description, priority, due_date])
                    else:
                        print("Skipping a line with missing or extra information.")
                except ValueError:
                    print("Skipping a corrupted line due to formatting issues.")
        print("Tasks loaded successfully!")
    except FileNotFoundError:
        print("No saved tasks found. Starting newly.")
    except Exception as e:
        print(f"Oops, something went wrong while loading tasks: {e}")


def save_tasks_to_file():
    #Saves tasks to a file
    try:
        with open("tasks.txt", "w") as file:
            for task in tasks:
                file.write(f"{task[0]},{task[1]},{task[2]},{task[3]}\n")
        print("All tasks have been saved successfully!")
    except Exception as e:
        print(f"An error occurred while saving tasks: {e}")


if __name__ == "__main__":
    #Runs the loop in CLI
    load_tasks_from_file()
    while True:
        print("\nTask Manager")
        print("==============")
        print("1. Add task")
        print("2. View tasks")
        print("3. Update task")
        print("4. Delete task")
        print("5. Save and Exit ")
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
            save_tasks_to_file()
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")
