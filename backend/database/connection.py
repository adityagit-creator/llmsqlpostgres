import psycopg2
from psycopg2 import Error
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        logging.info("Successfully connected to the PostgreSQL database.")
        return conn
    except Error as e:
        logging.error(f"Error connecting to PostgreSQL database: {e}")
        raise ConnectionError(f"Could not connect to database: {e}")

def execute_sql_query(sql_query: str):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql_query)
        if cur.description:
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            logging.info(f"SQL query executed successfully. Rows returned: {len(results)}")
            return {"columns": column_names, "rows": results}
        else:
            conn.commit()
            logging.info("SQL command executed successfully (no results to fetch).")
            return {"message": "SQL command executed successfully."}

    except Error as e:
        logging.error(f"Error executing SQL query '{sql_query}': {e}")
        if conn:
            conn.rollback()
        raise ValueError(f"Error executing SQL query: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            logging.info("Database connection closed.")
