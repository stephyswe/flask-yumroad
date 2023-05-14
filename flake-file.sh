#!/bin/bash

# This script runs isort, black, autoflake, and flake8 for specified files

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "Usage: ./flake.sh [file1.py] [file2.py] ..."
    exit 1
fi

for FILE in "$@"
do
  if [ ! -f "$FILE" ]
  then
    echo "File $FILE does not exist"
  else
    echo "Running isort, black, autoflake, and flake8 for $FILE"
    /home/stephy/yumroad-app/env/bin/isort "$FILE" && /home/stephy/yumroad-app/env/bin/autoflake --in-place --remove-unused-variables "$FILE" && /home/stephy/yumroad-app/env/bin/black "$FILE" && /home/stephy/yumroad-app/env/bin/flake8 "$FILE"
  fi
done
