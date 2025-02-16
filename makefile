# create a virtual environment
venv:
	python3 -m venv venv

# install dependencies from requirements.txt
install: venv
	./venv/bin/pip install -r requirements.txt

# run the download script to fetch crimes data and post script to insert data in the db
crimes:
	./venv/bin/python -m data.crimes.download
	./venv/bin/python -m data.criems.post

# run the generate script to generate officer's data and post script to insert data in the db
officers:
	./venv/bin/python -m data.officers.generate
	./venv/bin/python -m data.officers.post

# run the generate script to generate upvotes data and post script to insert data in the db
upvotes:
	./venv/bin/python -m data.upvotes.generate
	./venv/bin/python -m data.upvotes.post

# run the indexes script to create indexes in the db
indexes:
	./venv/bin/python -m db.indexes

# run the application
run:
	./venv/bin/python -m app.main

# setup all steps: create venv, install dependencies, and run the app
setup: venv install cimes officers upvotes indexes run

