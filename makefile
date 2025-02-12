# Create a virtual environment
venv:
	python3 -m venv venv

# Install dependencies from requirements.txt
install: venv
	./venv/bin/pip install -r requirements.txt

# Run the download script to fetch data
# download: install
# 	./venv/bin/python data/download.py
# ./venv/bin/python -m data.officers.generate

# Run the application
run:
	./venv/bin/python -m app.main

# Setup all steps: create venv, install dependencies, and run the app
setup: venv install run
# setup: venv install download run
