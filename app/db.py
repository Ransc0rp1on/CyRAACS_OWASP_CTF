# app/db.py
import os
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ctf_user:ctf_pass@db:5432/ctf_db"
)

def get_db_connection():
    """Return a new psycopg2 connection using DATABASE_URL."""
    return psycopg2.connect(DATABASE_URL)
