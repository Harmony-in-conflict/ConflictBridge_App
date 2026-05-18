from tkinter import messagebox

from app import MainApp
from database.db_connect import DBConnection
from database.db_setup import init_db


def main():
    try:
        init_db()
    except Exception as exc:
        messagebox.showerror(
            "Database setup failed",
            "CultureBridge needs PostgreSQL before it can start.\n\n"
            "Check that PostgreSQL is running and that your .env file matches .env.example.\n\n"
            f"Error: {exc}",
        )
        return

    app = MainApp()
    try:
        app.mainloop()
    finally:
        DBConnection.close_all()


if __name__ == "__main__":
    main()