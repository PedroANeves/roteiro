# roteiro
scrapes docx for roteiro timestamps and outputs a table.

## Running
### TLDR
install requirements
```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
run file with `python src/roteiro.py`
paste full filepath (or drag file to terminal) and hit enter

## Developing
You can develop this project using a multitude of ways, pick your poison.

## Tests
You can run tests in a multitude of ways:

### Using Makefile
`make test`

### Using VSCode test suite
Hit `ctrl+;` and `a` or hit `F1`, type `run all tests` and enter.

### By hand
create a venv, activate it and install development dependencies 
```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements-dev.txt
pytest src
```
Open [Coverage report](./htmlcov/index.html).
