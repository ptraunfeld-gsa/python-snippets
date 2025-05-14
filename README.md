# Python Snippets

## Setup Virtual Environment and Install Dependencies

```sh
# Create a virtual environment named "venv"
python -m venv venv

# Activate the virtual environment on Windows:
. ./venv/Scripts/activate

#  Activate the virtual environment on Mac:
. ./venv/bin/activate

# Install requirements
python -m pip install -r requirements.txt
```

## Testing
```sh
# Run a test
python -m unittest validate_jwt_test

# Run all test files verbosely
python -m unittest discover -p "*test.py" -v

# Run a test with branch coverage 
python -m coverage run --branch validate_jwt_test.py

# View coverage report
python -m coverage report 
```