from contextlib import contextmanager
from pathlib import Path
import os

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


class DBConnection:
    """Shared PostgreSQL connection pool for the Tkinter application."""

    _pool = None

    @classmethod
    def init_pool(cls):
        if cls._pool is not None:
            return

        database = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        if not database or not user or password is None:
            raise RuntimeError(
                "Database settings are missing. Copy .env.example to .env and fill in DB_NAME, DB_USER, and DB_PASSWORD."
            )

        cls._pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=20,
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=database,
            user=user,
            password=password,
        )

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.init_pool()
        return cls._pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        if cls._pool is not None and conn is not None:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None

    @classmethod
    @contextmanager
    def cursor(cls, commit=False, dict_cursor=True):
        conn = cls.get_connection()
        cursor_factory = RealDictCursor if dict_cursor else None
        cur = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cur
            if commit:
                conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            cls.return_connection(conn)

# This file provides a shared database connection pool for the Tkinter application. It uses psycopg2's 
# SimpleConnectionPool to manage connections to a PostgreSQL database. The connection settings are loaded from a .env file, 
# and the class provides methods to get and return connections,
#  as well as a context manager for executing queries with automatic commit and rollback handling.