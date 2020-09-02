# Consortium Capability-based Access control system

A PhD project to create a light weight access control based on tokens and blockchain to leverage AC for IoT 

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Python and project related models.
Better to work with a python virtual env like pipenv

```bash
pip install pipenv
```
Install all dependencies for the project from inside the project directory
```bash
pipenv install --dev
```
Lunch Flask app (instruction for windows users) Ubuntu change 'set' by 'export'
```bash
set FLASK_APP=app.py
set FLASK_DEBUG = 1 (optional)
flask run
```

## Usage

### Open your browser and enter the address:

http://127.0.0.1:5000/

### Enter the Admin token:

"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1vaGFtaW5lMTgiLCJwYXNzd29yZCI6IjE5OTEifQ.Q6JDqfYHVwzRYzGFLiFmfmFaD5cU3mEYjIx8Ft-XPic"

### You are ready to explore the system