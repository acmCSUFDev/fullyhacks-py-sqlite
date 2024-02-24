# fullyhacks-py-sqlite

SQLite example in Python for the FullyHacks workshop.

> [!NOTE]
> This example doesn't just use SQLite, but also uses Pydantic to bridge the
> SQLite table to Python objects in a more Pythonic way. For information on
> Pydantic, see [Pydantic's documentation](https://docs.pydantic.dev/latest/).

## Learning

The SQLite example is in the `main.py` file. The `main.py` file contains a
simple example of how to use SQLite in Python to manage tables and store and
retrieve data.

## Running

First, ensure you have Python 3 installed. Then, enter the virtual environment
and install the dependencies:

```sh
# Enter the virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

Then, run the script:

```sh
python -m main
```

> [!NOTE]
> If `python` is not found, try `python3` instead, or `python.exe` or
> `python3.exe` on Windows.
