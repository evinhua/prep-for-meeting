#!/usr/bin/env python
import os
import sys

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Print absolute path of this script
print(f"Script path: {os.path.abspath(__file__)}")

# Print parent directory (should be the api directory)
api_dir = os.path.dirname(os.path.abspath(__file__))
print(f"API directory: {api_dir}")

# Print project root (one level up from api directory)
project_root = os.path.abspath(os.path.join(api_dir, '..'))
print(f"Project root: {project_root}")

# Check if the project root exists
print(f"Project root exists: {os.path.exists(project_root)}")

# List files in the project root
print(f"Files in project root: {os.listdir(project_root)}")

# Check if src directory exists
src_dir = os.path.join(project_root, 'src')
print(f"src directory exists: {os.path.exists(src_dir)}")

# Check if main.py exists
main_py = os.path.join(project_root, 'src', 'prep_for_meeting', 'main.py')
print(f"main.py exists: {os.path.exists(main_py)}")

# Print Python path
print(f"Python path: {sys.path}")
