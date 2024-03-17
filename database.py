import os
import sqlite3
import sys

from . import Constants
from . import queries

DB_FILE = f"{os.getenv("USERPROFILE")}{Constants.SLASH}Vault{Constants.SLASH}master.db"


def create_db(verifier_string: str):
    # creating empty db file
    open(DB_FILE, "w").close()

    try:
        conn = sqlite3.connect(DB_FILE)

        # creating required tables
        conn.execute(queries.CREATE_TABLE_CONSTANTS)
        conn.execute(queries.CREATE_TABLE_FILE_DATA)
        conn.execute(queries.CREATE_TABLE_OBJECT_DATA)

        # inserting verifier string
        cur = conn.cursor()
        cur.execute(queries.INSERT_INTO_CONSTANTS, ("verifier_string", verifier_string))
    except sqlite3.Error as e:
        print(e)
        sys.exit(1)
    finally:
        if conn:
            conn.commit()
            conn.close()


def verify_db() -> bool:
    required_table_sql = [
        ("constants", queries.CREATE_TABLE_CONSTANTS),
        ("file_data", queries.CREATE_TABLE_FILE_DATA),
        ("object_data", queries.CREATE_TABLE_OBJECT_DATA),
    ]

    verified = True
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        # checking tables sql
        for table_name, table_sql in required_table_sql:
            cur.execute(queries.GET_TABLES_INFO, (table_name,))
            result = cur.fetchone()
            if result is None or (result is not None and result[0] != table_sql):
                verified = False
                break
    except sqlite3.Error:
        verified = False
    finally:
        if conn:
            conn.close()

    return verified


def get_verifier_string() -> str:
    verifier_string = ""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute(queries.GET_CONSTANT, ("verifier_string",))
        result = cur.fetchone()
        if result is not None:
            verifier_string = result[0]
    except sqlite3.Error:
        verifier_string = ""
    finally:
        if conn:
            conn.close()

    return verifier_string
