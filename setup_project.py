import os

# Define the root directory for the project
ROOT_DIR = "ai_scheduling_agent"

# List of directories to be created
# The os.path.join function creates paths that work across different operating systems.
DIRECTORIES = [
    os.path.join(ROOT_DIR, "app"),
    os.path.join(ROOT_DIR, "agent"),
    os.path.join(ROOT_DIR, "tools"),
    os.path.join(ROOT_DIR, "data"),
    os.path.join(ROOT_DIR, "data/intake_forms"),
    os.path.join(ROOT_DIR, "utils"),
]

# List of files to be created
# These will be created as empty files.
FILES = [
    os.path.join(ROOT_DIR, "app/main.py"),
    os.path.join(ROOT_DIR, "agent/__init__.py"),
    os.path.join(ROOT_DIR, "agent/state.py"),
    os.path.join(ROOT_DIR, "agent/nodes.py"),
    os.path.join(ROOT_DIR, "agent/graph.py"),
    os.path.join(ROOT_DIR, "tools/__init__.py"),
    os.path.join(ROOT_DIR, "tools/db_tools.py"),
    os.path.join(ROOT_DIR, "tools/calendar_tools.py"),
    os.path.join(ROOT_DIR, "tools/file_tools.py"),
    os.path.join(ROOT_DIR, "tools/communication_tools.py"),
    os.path.join(ROOT_DIR, "data/patients.csv"),
    os.path.join(ROOT_DIR, "data/doctor_schedules.xlsx"),
    os.path.join(ROOT_DIR, "utils/data_generator.py"),
    os.path.join(ROOT_DIR, ".env"),
    os.path.join(ROOT_DIR, ".gitignore"),
    os.path.join(ROOT_DIR, "config.py"),
    os.path.join(ROOT_DIR, "requirements.txt"),
    os.path.join(ROOT_DIR, "README.md"),
]

def create_project_structure():
    """Generates the directories and files for the project."""
    print(f"Creating project structure for '{ROOT_DIR}'...")

    # Create the root directory first
    os.makedirs(ROOT_DIR, exist_ok=True)

    # Create all sub-directories
    for directory in DIRECTORIES:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"  Created directory: {directory}")
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")

    # Create all the empty files
    for file_path in FILES:
        try:
            # 'a' mode creates the file if it doesn't exist without overwriting.
            with open(file_path, 'a'):
                pass
            print(f"  Created file:      {file_path}")
        except IOError as e:
            print(f"Error creating file {file_path}: {e}")

    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()