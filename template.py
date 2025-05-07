"""
This script creates a directory structure for a Python project named "linprog".
It includes directories for different linear programming methods, utilities, logs, and a template file.
The script also creates an empty README file and a setup.py file for package configuration.
The script uses the `os` module to create directories and files, and the `logging` module to log the creation of directories and files.
The script is designed to be run in a Python environment and will create the necessary directories and files if they do not already exist.
"""

import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_NAME = "linprog"

list_of_files = [
    # Init files to mark directories as Python packages
    "linprog/__init__.py",
    "linprog/method/__init__.py",
    "linprog/method/geometric/__init__.py",
    "linprog/method/simplex/__init__.py",
    "linprog/method/bland/__init__.py",
    "linprog/method/two_phase/__init__.py",
    "linprog/method/config/__init__.py",
    "utils/__init__.py",
    "linprog/llms_feat/__init__.py",

    # Main files
    "app.py",

    # Data and research
    "data/.gitkeep",
    "research/.gitkeep",

    # Logs
    "logs/linprog.log",

    # Method directory with various methods
    "linprog/method/config/configuration.py",
    "linprog/method/geometric/components.py",
    "linprog/method/geometric/solver.py",
    "linprog/method/geometric/explain.py",
    "linprog/method/geometric/main.py",
    "linprog/method/simplex/components.py",
    "linprog/method/simplex/solver.py",
    "linprog/method/simplex/explain.py",
    "linprog/method/simplex/main.py",
    "linprog/method/bland/components.py",
    "linprog/method/bland/solver.py",
    "linprog/method/bland/explain.py",
    "linprog/method/bland/main.py",
    "linprog/method/two_phase/components.py",
    "linprog/method/two_phase/solver.py",
    "linprog/method/two_phase/explain.py",
    "linprog/method/two_phase/main.py",

    # LLMs features (placeholder)
    "linprog/llms_feat/.gitkeep",

    # Utilities
    "utils/logger.py",
    "utils/common.py",

    # Reference documents
    "reference/.gitkeep",

    # Project setup file
    "setup.py",
    
    # Project template
    "template.py"
]

for file_path in list_of_files:
    file_dir = os.path.dirname(file_path)

    if file_dir and not os.path.exists(file_dir):
        os.makedirs(file_dir)
        logging.info("Directory created: %s", file_dir)
    elif file_dir:
        logging.info("Directory already exists: %s", file_dir)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            pass
        logging.info("File created: %s", file_path)
    else:
        logging.info("File already exists: %s", file_path)
