#!/usr/bin/env python3
"""Standalone admin-creation script.

This script runs outside the Flask app. It connects to the database specified
by the `DATABASE_URL` environment variable (or `sqlite:///blog.db` by default),
hashes the provided password with bcrypt, and inserts or promotes a user to
role='admin'.

Usage examples:
  python scripts/create_admin_standalone.py --email admin@example.com --name "Site Admin"
  python scripts/create_admin_standalone.py --email admin@example.com --password S3cret

If `--password` is omitted the script will prompt for it securely.
"""

import argparse
import os
from datetime import datetime
from getpass import getpass

import bcrypt
from sqlalchemy import create_engine, text


def prompt_password():
    while True:
        pw = getpass("Password: ")
        pw2 = getpass("Confirm Password: ")
        if pw != pw2:
            print("Passwords do not match. Try again.")
            continue
        if len(pw) < 6:
            print("Password must be at least 6 characters.")
            continue
        return pw


def get_database_url():
    return os.environ.get("DATABASE_URL", "sqlite:///instance/blog.db")


def main():
    parser = argparse.ArgumentParser(description="Create or promote an admin user (standalone)")
    parser.add_argument("--email", required=True, help="Admin user's email")
    parser.add_argument("--name", required=False, help="Admin user's name")
    parser.add_argument("--password", required=False, help="Password for the admin user (will prompt if omitted)")

    args = parser.parse_args()
    password = args.password or prompt_password()

    db_url = get_database_url()
    engine = create_engine(db_url)

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with engine.connect() as conn:
        # Ensure users table exists
        # Check for existing user
        sel = text("SELECT id, name, email FROM users WHERE email = :email")
        res = conn.execute(sel, {"email": args.email}).mappings().fetchone()

        now = datetime.utcnow()

        if res:
            user_id = res["id"]
            print(f"User with email {args.email} already exists (id={user_id}). Promoting to admin and updating password.")
            upd = text(
                "UPDATE users SET name = :name, password = :password, role = 'admin', updated_at = :updated_at WHERE id = :id"
            )
            conn.execute(upd, {"name": args.name or res["name"], "password": hashed, "updated_at": now, "id": user_id})
            conn.commit()
            print(f"Updated user id={user_id} -> role=admin")
        else:
            ins = text(
                "INSERT INTO users (name, email, password, role, created_at, updated_at) VALUES (:name, :email, :password, 'admin', :created_at, :updated_at)"
            )
            result = conn.execute(ins, {"name": args.name or "Admin", "email": args.email, "password": hashed, "created_at": now, "updated_at": now})
            conn.commit()
            # SQLite: lastrowid on result
            try:
                user_id = result.lastrowid
            except Exception:
                # Fallback: query the user id
                q = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": args.email}).mappings().fetchone()
                user_id = q["id"] if q else None
            print(f"Created admin user '{args.email}' (id={user_id})")


if __name__ == "__main__":
    main()
