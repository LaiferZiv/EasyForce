# EasyForce

## Project Overview
EasyForce is a command-line tool for managing teams, soldiers and task scheduling information using a local SQLite database. It includes utilities for initializing the database schema, CRUD operations on entities (like teams or tasks) and an interactive interface for adding or displaying records. The project is currently an internal CLI service, with future plans to package it so that users can download and run it as a standalone application.

## Features and Functionality
- **Database Initialization** – scripts under `data_management/init_db` create entity tables, relationship tables and triggers.
- **Entity Models** – classes in `data_management/data_structure` provide CRUD operations through a shared `BaseEntity` helper.
- **CLI Interface** – `interface/main_interface.py` offers a text menu for adding teams, soldiers and tasks, along with displaying database tables.
- **Utility Helpers** – functions in `common/utils.py` assist with input validation and question workflows.

## Architecture and Structure
```
EasyForce/
├── EasyForce/
│   ├── common/                 # config constants and helper utilities
│   ├── data_management/        # database models and initialization
│   ├── data_processing/        # scheduling logic (stub)
│   ├── interface/              # command-line interface modules
│   └── main.py                 # project entry point
└── tests/                      # basic pytest tests
```
Key files include:
- `main.py` – launches database initialization then invokes the CLI menu.
- `read_db.py` – helper functions for reading and displaying database contents.
- `init_db/*.py` – scripts creating tables for entities, relationships and triggers.

The project relies on the Python standard library (e.g., `sqlite3`) and does not require external dependencies.

## Setup Instructions
1. Clone the repository and move into the directory:
   ```bash
   git clone <repo-url>
   cd EasyForce
   ```
2. (Optional) create a virtual environment and install any future dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # if such a file is added
   ```
3. Run the application:
   ```bash
   python EasyForce/main.py
   ```
   The script will create `my_database.db` in the project root and open an interactive menu.

## Current Tasks & TODOs
- **Scheduling Logic** – `data_processing/schedule_logic.py` only defines a stub `schedule_shifts()` function.
- **Update/Delete Workflows** – functions in `interface/user_questions_management/update_questions` and `delete_questions` are mostly empty placeholders.
- **Additional Relationship Features** – `add_currentTaskAssignment_questions` and `add_TaskHistory_questions` (in `add_relationships.py`) print "not yet implemented" messages.
- **Refactoring** – `read_db.py` contains a comment about rewriting the `get_primary_key_column_names` helper.
- **Testing** – expand coverage. The example under `tests/` now imports modules correctly but covers only minimal behaviour.

## Suggestions for Improvements
- Implement command line argument parsing or configuration for easier customization.
- Introduce structured logging and better error handling in place of print statements.
- Package the project so users can install it as a standalone application (e.g. using PyInstaller or a simple pip install).
- Integrate continuous integration to automatically run tests on pull requests.

## How to Contribute
Contributions are welcome! Fork the repository and submit a pull request. Please open an issue first for major changes to discuss your proposal.
