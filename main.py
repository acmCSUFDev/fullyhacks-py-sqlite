#!/usr/bin/env python3
import sqlite3
from doc import fprint
from typing import Optional
from pydantic import BaseModel

# Create a new SQLite database.
db = sqlite3.connect("test.db", check_same_thread=False)
db.row_factory = sqlite3.Row

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


class User(BaseModel):
    id: int
    username: str
    password: str
    bio: Optional[str] = None


def main():
    # First, set up the database by executing the schema.
    db.executescript(DB_SCHEMA)
    db.commit()

    # Add some users.
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("alice", "1234"),
    )
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("bob", "1234"),
    )
    db.commit()

    # Print Alice.

    # First, we fetch the row from the database.
    # This returns a raw SQLite row object.
    alice_row = db.execute(
        "SELECT * FROM users WHERE username = ?",
        ("alice",),
    ).fetchone()

    # Then, we parse the row into a User object.
    alice = User(**alice_row)

    # Finally, we print the user.
    fprint("Alice:", alice)

    # Do the same for all users. We can use list comprehension to make this
    # more concise.
    user_rows = db.execute("SELECT * FROM users").fetchall()
    users = [User(**row) for row in user_rows]
    fprint("Users:", users)

    # Make our life easier by creating a function to fetch users.
    def get_user(username: str) -> User | None:
        row = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        # row may be None if the user does not exist.
        return User(**row) if row else None

    # Give Alice a bio.
    db.execute("UPDATE users SET bio = ? WHERE username = ?", ("I am Alice", "alice"))
    db.commit()

    # Print Alice again to see the changes.
    alice = get_user("alice")
    fprint("Alice:", alice)

    # Delete Bob.
    db.execute("DELETE FROM users WHERE username = ?", ("bob",))
    db.commit()

    # Observe that Bob is gone.
    bob = get_user("bob")
    fprint("Bob:", bob)


if __name__ == "__main__":
    main()
