#!/bin/bash

# This script runs isort, black, autoflake, and flake8 for specified files

if [ $# -eq 0 ]; then
  echo "No arguments supplied"
  echo "Usage: ./flake.sh [file1.py] [file2.py] ... OR ./flake.sh [dir1/] [dir2/] ..."
  exit 1
fi

venv_path="/home/stephy/yumroad-app/env/bin"

function process_file() {
  local file="$1"
  if grep -q "print(" "$file"; then
    echo "Error: $file contains print() statement"
    return
  fi
  "$venv_path/isort" "$file"
  "$venv_path/autoflake" --in-place --remove-unused-variables "$file"
  "$venv_path/black" "$file" &>/dev/null
  "$venv_path/flake8" "$file" > /dev/null
}

for arg in "$@"; do
  if [ -d "$arg" ]; then
    echo "Processing directory $arg"
    find "$arg" -name '*.py' -type f -print0 | while read -d $'\0' file; do
      process_file "$file"
    done
  elif [ -f "$arg" ]; then
    process_file "$arg"
  else
    echo "Error: $arg is not a file or directory"
  fi
done
