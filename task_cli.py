# The following imports bring in needed functionality:
# - sys: For accessing command-line arguments and interacting with the Python interpreter.
# - json: For reading from and writing to JSON files (where tasks are stored).
# - os: For working with the file system (e.g., checking if the tasks file exists).
# - datetime: For handling date and time information (such as task timestamps).
import sys
import json
import os
from datetime import datetime

# The name of the file where tasks are stored
TASKS_FILE = "tasks.json"

def now_iso():
    # e.g., "2025-10-16T18:20:05"
    return datetime.now().isoformat(timespec="seconds")

def load_tasks():
    """Load tasks from the JSON file or return an empty list if file doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        # If file is empty or corrupted, start fresh instead of crashing
        return []

def save_tasks(tasks):
    """Save tasks back into the JSON file."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def next_id(tasks):
    """Return the next integer id."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

def find_task(tasks, tid):
    """Return (task, index) or (None, -1) if not found."""
    for i, t in enumerate(tasks):
        if t.get("id") == tid:
            return t, i
    return None, -1

def set_status(tasks, tid, new_status):
    """Set task status and bump updatedAt. Return True if changed, else False."""
    t, _ = find_task(tasks, tid)
    if not t:
        return False
    t["status"] = new_status
    t["updatedAt"] = now_iso()
    save_tasks(tasks)
    return True


def handle_add(args):
    """Add a new task with a description."""
    if len(args) < 2:
        print("Usage: python task_cli.py add \"Task description\"")
        return
    description = args[1].strip()
    if not description:
        print("Error: Description cannot be empty.")
        return

    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "description": description,
        "status": "todo",              # todo | in-progress | done
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")

def handle_list(args):
    """List tasks, optionally filtered by status."""
    valid_status = {"todo", "in-progress", "done"}
    # args[0] = "list"; args[1] may be a status
    status_filter = None
    if len(args) >= 2:
        candidate = args[1].strip().lower()
        if candidate not in valid_status:
            print("Usage: python task_cli.py list [todo|in-progress|done]")
            return
        status_filter = candidate

    tasks = load_tasks()
    if status_filter:
        tasks = [t for t in tasks if t.get("status") == status_filter]

    if not tasks:
        print("No tasks found.")
        return

    # Pretty-print
    print(f"{'ID':<4} {'STATUS':<12} {'UPDATED':<19} DESCRIPTION")
    print("-" * 70)
    for t in tasks:
        tid = t.get("id")
        status = t.get("status", "")
        updated = t.get("updatedAt", "")[:19]  # trim seconds format if longer
        desc = t.get("description", "")
        print(f"{tid:<4} {status:<12} {updated:<19} {desc}")

def handle_update(args):
    """Update a task's description by id."""
    # Expected: update <id> "new description"
    if len(args) < 3:
        print('Usage: python task_cli.py update <id> "New description"')
        return

    # Parse id safely
    try:
        tid = int(args[1])
    except ValueError:
        print("Error: <id> must be a number.")
        return

    new_desc = args[2].strip()
    if not new_desc:
        print("Error: Description cannot be empty.")
        return

    tasks = load_tasks()
    # Find task
    for t in tasks:
        if t.get("id") == tid:
            t["description"] = new_desc
            t["updatedAt"] = now_iso()
            save_tasks(tasks)
            print(f"Task {tid} updated successfully.")
            return

    print(f"Error: Task with ID {tid} not found.")

def handle_mark_in_progress(args):
    """Mark a task as in-progress by id."""
    if len(args) < 2:
        print("Usage: python task_cli.py mark-in-progress <id>")
        return
    try:
        tid = int(args[1])
    except ValueError:
        print("Error: <id> must be a number.")
        return

    tasks = load_tasks()
    if set_status(tasks, tid, "in-progress"):
        print(f"Task {tid} marked as in-progress.")
    else:
        print(f"Error: Task with ID {tid} not found.")

def handle_mark_done(args):
    """Mark a task as done by id."""
    if len(args) < 2:
        print("Usage: python task_cli.py mark-done <id>")
        return
    try:
        tid = int(args[1])
    except ValueError:
        print("Error: <id> must be a number.")
        return

    tasks = load_tasks()
    if set_status(tasks, tid, "done"):
        print(f"Task {tid} marked as done.")
    else:
        print(f"Error: Task with ID {tid} not found.")

def handle_delete(args):
    """Delete a task by id."""
    if len(args) < 2:
        print("Usage: python task_cli.py delete <id>")
        return
    try:
        tid = int(args[1])
    except ValueError:
        print("Error: <id> must be a number.")
        return

    tasks = load_tasks()
    # Find index
    idx = next((i for i, t in enumerate(tasks) if t.get("id") == tid), -1)
    if idx == -1:
        print(f"Error: Task with ID {tid} not found.")
        return

    tasks.pop(idx)
    save_tasks(tasks)
    print(f"Task {tid} deleted successfully.")

def print_help():
    usage = """
Task Tracker CLI (task_cli.py)

Usage:
  python task_cli.py add "Description"
  python task_cli.py list [todo|in-progress|done]
  python task_cli.py update <id> "New description"
  python task_cli.py delete <id>
  python task_cli.py mark-in-progress <id>
  python task_cli.py mark-done <id>
  python task_cli.py help

Notes:
  - Tasks are stored in tasks.json in this folder.
  - Status values: todo | in-progress | done
  - Timestamps: createdAt, updatedAt (ISO format)

Examples:
  python task_cli.py add "Buy groceries"
  python task_cli.py list
  python task_cli.py list done
  python task_cli.py update 1 "Buy groceries and cook dinner"
  python task_cli.py mark-in-progress 1
  python task_cli.py mark-done 1
  python task_cli.py delete 1
"""
    print(usage.strip())

def handle_help(_args):
    print_help()

def main():
    """Main entry point for our CLI."""
    # sys.argv holds everything typed after 'python task_cli.py'
    args = sys.argv[1:]

    if not args:
        print("Please provide a command, e.g. 'add', 'list', or 'delete'")
        return

    command = args[0]

    if command == "add":
        handle_add(args)
    elif command == "list":
        handle_list(args)
    elif command == "update":
        handle_update(args)
    elif command == "delete":
        handle_delete(args)
    elif command == "mark-in-progress":
        handle_mark_in_progress(args)
    elif command == "mark-done":
        handle_mark_done(args)
    elif command == "help":
        handle_help(args)
    else:
        print(f"Unknown command: {command}. Try: python task_cli.py help")

if __name__ == "__main__":
    main()
