## Task Tracker CLI
https://roadmap.sh/projects/task-tracker

Simple task tracker managed from the command line. Tasks are stored locally in `tasks.json` in this folder. No external dependencies.

## Requirements

- Python 3.10+ (works with Python 3.13)
- macOS/Linux/Windows supported

## Quick start

1. Optional: create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
```

2. Run the CLI

```bash
python task_cli.py help
```

## Usage

```bash
python task_cli.py add "Description"
python task_cli.py list [todo|in-progress|done]
python task_cli.py update <id> "New description"
python task_cli.py delete <id>
python task_cli.py mark-in-progress <id>
python task_cli.py mark-done <id>
python task_cli.py help
```

## Examples

```bash
# Add a task
python task_cli.py add "Buy groceries"

# List tasks
python task_cli.py list

# List only done tasks
python task_cli.py list done

# Update description
python task_cli.py update 1 "Buy groceries and cook dinner"

# Change status
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# Delete a task
python task_cli.py delete 1
```

## Data model

Tasks are stored in `tasks.json` as an array of objects with the following fields:

- **id**: auto-incrementing integer
- **description**: free text
- **status**: one of `todo`, `in-progress`, `done`
- **createdAt**: ISO datetime string
- **updatedAt**: ISO datetime string

Example entry:

```json
{
  "id": 1,
  "description": "Buy some beer",
  "status": "in-progress",
  "createdAt": "2025-10-16T21:45:27",
  "updatedAt": "2025-10-17T17:04:02"
}
```

## Notes

- If `tasks.json` is missing or corrupted, the CLI starts with an empty list.
- Use `python task_cli.py help` to see commands at any time.
