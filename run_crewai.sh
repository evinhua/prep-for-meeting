#!/bin/bash

# Print current directory
echo "Running in directory: $(pwd)"

# Set up environment
export PATH="/Users/evinhua/genai/bin:$PATH"
echo "PATH: $PATH"

# Check if crewai is in PATH
which crewai
if [ $? -ne 0 ]; then
  echo "crewai not found in PATH"
  exit 1
fi

# Run crewai command with verbose output
echo "Running: crewai run"
crewai run

# Check exit status
exit_status=$?
echo "Command exit status: $exit_status"

# Check if report.md was created
if [ -f "report.md" ]; then
  echo "report.md was created successfully"
  echo "Content of report.md:"
  cat report.md
else
  echo "report.md was not created"
fi

# List all files in current directory
echo "Files in current directory:"
ls -la

exit $exit_status
