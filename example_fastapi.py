#!/usr/bin/env python3
from contextlib import asynccontextmanager
from typing import Optional
import pydantic
import sqlite3
import uvicorn
import fastapi
import fastapi.responses

# Define the schema for the database.
# This is executed every time the program is run, so we have to check if the
# table already exists.
DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        bio TEXT
    );
"""

# Set the name of the database file.
# Ideally, use "database.db" or something similar, but for the sake of the
# example, we'll use ":memory:" to create a temporary database.
DB_FILE = ":memory:"


# Create a new SQLite database.
db = sqlite3.connect(DB_FILE, check_same_thread=False)
db.row_factory = sqlite3.Row


class User(pydantic.BaseModel):
    """
    This class represents a user.

    It closely mirrors the database schema and allows us to easily work with
    SQLite rows from that table.
    """

    id: int
    username: str
    password: str
    bio: Optional[str] = None


@asynccontextmanager
async def init_db(_: fastapi.FastAPI):
    """
    Initialize the database before FastAPI starts
    then continue starting it.
    """
    db.executescript(DB_SCHEMA)
    db.commit()
    yield


# Create our FastAPI app.
app = fastapi.FastAPI(lifespan=init_db)


@app.get("/users")
def get_users() -> list[User]:
    """
    Get all users from the database.
    """
    cursor = db.execute("SELECT * FROM users")
    return [User(**row) for row in cursor.fetchall()]


class AddUserRequest(pydantic.BaseModel):
    """
    This class represents the request body for adding a user.
    """

    username: str
    password: str
    bio: Optional[str] = None


@app.post("/users")
def add_user(request: AddUserRequest) -> User:
    """
    Add a user to the database.
    """
    row = db.execute(
        "INSERT INTO users (username, password, bio) VALUES (?, ?, ?) RETURNING id",
        (request.username, request.password, request.bio),
    ).fetchone()
    db.commit()

    return User(
        id=row["id"],
        username=request.username,
        password=request.password,
        bio=request.bio,
    )


@app.get("/")
def index() -> fastapi.responses.RedirectResponse:
    """
    Redirect to the documentation.
    """
    return fastapi.responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run("example_fastapi:app", host="127.0.0.1", port=5700)
