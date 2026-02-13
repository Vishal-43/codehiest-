#!/bin/bash

PROJECT_NAME="collab_portal"

echo "Creating project structure..."

mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# Root files
touch main.py
touch database.py
touch models.py
touch schemas.py
touch crud.py
touch requirements.txt

# Directories
mkdir -p templates
mkdir -p static
mkdir -p uploads

# Template files
touch templates/base.html
touch templates/dashboard.html
touch templates/project_detail.html
touch templates/task_detail.html
touch templates/create_project.html
touch templates/create_task.html

# Static files
touch static/styles.css

echo "Structure created successfully."
