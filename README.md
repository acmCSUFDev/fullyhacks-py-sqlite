# fullyhacks-py-sqlite

SQLite example in Python for the FullyHacks workshop.

> [!NOTE]
> This example doesn't just use SQLite, but also uses Pydantic to bridge the
> SQLite table to Python objects in a more Pythonic way. For information on
> Pydantic, see [Pydantic's documentation](https://docs.pydantic.dev/latest/).

> [!IMPORTANT]
> The `users` table in the example is not secure: it stores passwords in plain
> text. In the real world, **you should never store passwords in plain text**.
> Use a secure hashing algorithm like bcrypt or PBKDF2 instead.

## Learning

The SQLite example is in the `example.py` file. The `example.py` file contains a
simple example of how to use SQLite in Python to manage tables and store and
retrieve data.

If you're here for the FastAPI example, see `example_fastapi.py` for a simple
example of how to use SQLite with FastAPI to create a simple RESTful API.

## Running

First, ensure you have Python 3 installed. Then, enter the virtual environment
and install the dependencies:

```sh
# Enter the virtual environment (instructions differ on Windows, see
# https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html)
python -m venv .venv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

Then, run the example:

```sh
python -m example
```

If you want to run the FastAPI example, run:

```sh
python -m example_fastapi
```

or

```sh
uvicorn example_fastapi:app --reload
```

> [!NOTE]
> If `python` is not found, try `python3` instead, or `python.exe` or
> `python3.exe` on Windows.

> [!NOTE]
> We provide a Nix Flake file! Simply run `nix develop` to enter the development
> environment, install the dependencies, and run the example.
