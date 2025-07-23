# llm-sql-chatbot/backend/services/sql_agent.py
# This module orchestrates the LLM to generate and execute SQL queries.
# ---
# Corrected import to be absolute relative to the 'backend' package
from backend.services.llm_service import LLMService
from backend.database.connection import execute_sql_query
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SQLAgent:
    """
    Agent responsible for translating natural language to SQL and executing it.
    """
    def __init__(self):
        self.llm_service = LLMService()
        # Define a system prompt to guide the LLM in generating SQL queries.
        # It's crucial to provide schema information for accurate SQL generation.
        self.system_prompt = """
        You are an AI assistant that translates natural language questions into PostgreSQL SQL queries.
        You should only respond with the SQL query itself, and nothing else.
        Do not include any explanations, comments, or extra text.
        Crucially, **only generate SELECT, INSERT, UPDATE, or DELETE statements.**
        **NEVER generate CREATE, ALTER, DROP, TRUNCATE, GRANT, REVOKE, or any other DDL/DCL commands.**
        If you cannot generate a valid SQL query for the given request (adhering to the allowed types), respond with 'INVALID_QUERY'.

        Here is the database schema:
        TABLE users:
        - id INT PRIMARY KEY
        - name VARCHAR(255)
        - email VARCHAR(255) UNIQUE
        - created_at TIMESTAMP

        TABLE products:
        - id INT PRIMARY KEY
        - name VARCHAR(255)
        - price DECIMAL(10, 2)
        - stock INT

        TABLE orders:
        - id INT PRIMARY KEY
        - user_id INT (FOREIGN KEY to users.id)
        - product_id INT (FOREIGN KEY to products.id)
        - quantity INT
        - order_date TIMESTAMP

        Example:
        User: "Show me all users"
        SQL: SELECT * FROM users;

        User: "How many products cost more than 50?"
        SQL: SELECT COUNT(*) FROM products WHERE price > 50;

        User: "What are the names of products ordered by John Doe?"
        SQL: SELECT p.name FROM products p JOIN orders o ON p.id = o.product_id JOIN users u ON o.user_id = u.id WHERE u.name = 'John Doe';

        User: "Add a new user named Alice with email alice@example.com and id 3"
        SQL: INSERT INTO users (id, name, email, created_at) VALUES (3, 'Alice', 'alice@example.com', NOW());

        User: "Increase the stock of Laptop by 10"
        SQL: UPDATE products SET stock = stock + 10 WHERE name = 'Laptop';

        User: "Delete the user with id 1"
        SQL: DELETE FROM users WHERE id = 1;

        User: "Find products with stock less than 20"
        SQL: SELECT name, stock FROM products WHERE stock < 20;
        """

    def _extract_sql_from_llm_response(self, llm_response: str) -> str:
        """
        Extracts and validates the SQL query from the LLM's response.
        Ensures the response is a single, allowed SQL DML statement.
        """
        sql_query = llm_response.strip()

        # Check for empty or 'INVALID_QUERY' response from LLM
        if not sql_query or sql_query == "INVALID_QUERY":
            logging.warning("LLM returned an empty or 'INVALID_QUERY' response.")
            return "INVALID_QUERY"

        # Define allowed DML (Data Manipulation Language) keywords
        allowed_dml_keywords = r'^\s*(SELECT|INSERT|UPDATE|DELETE)\b'
        
        # Define disallowed DDL (Data Definition Language) and DCL (Data Control Language) keywords
        # This is a critical security measure to prevent schema modifications or privilege changes.
        disallowed_keywords = r'\b(CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE|VACUUM|REINDEX|REFRESH)\b'

        # Check if the query starts with an allowed DML keyword
        if not re.match(allowed_dml_keywords, sql_query, re.IGNORECASE):
            logging.warning(f"Generated SQL does not start with an allowed DML keyword: {sql_query}")
            return "UNSAFE_QUERY"

        # Check for any disallowed keywords within the query
        if re.search(disallowed_keywords, sql_query, re.IGNORECASE):
            logging.warning(f"Generated SQL contains disallowed keywords: {sql_query}")
            return "UNSAFE_QUERY"
        
        # Basic check to ensure it looks like a single statement (ends with a semicolon, though not strictly required by psycopg2)
        # This helps prevent multiple statements being generated
        if ';' in sql_query.strip(' ;') and sql_query.strip().count(';') > 1:
            logging.warning(f"Generated SQL contains multiple statements: {sql_query}")
            return "UNSAFE_QUERY"

        return sql_query

    async def process_query(self, natural_language_query: str): # Made async
        """
        Processes a natural language query:
        1. Prompts the LLM to generate a SQL query.
        2. Executes the generated SQL query.
        3. Returns the results.
        """
        try:
            # Step 1: Generate SQL query using LLM
            full_prompt = f"{self.system_prompt}\nUser: \"{natural_language_query}\"\nSQL:"
            logging.info(f"Sending prompt to LLM: {full_prompt}")
            llm_raw_response = await self.llm_service.generate_text(full_prompt) # Await the async call
            sql_query = self._extract_sql_from_llm_response(llm_raw_response)
            logging.info(f"LLM generated SQL: {sql_query}")

            if sql_query == "INVALID_QUERY":
                return {"error": "Could not generate a valid SQL query from your request. Please rephrase or provide more context."}
            elif sql_query == "UNSAFE_QUERY":
                # Provide a more specific error message for disallowed queries
                return {"error": "Generated query contains disallowed operations. Only SELECT, INSERT, UPDATE, and DELETE are permitted."}

            # Step 2: Execute the SQL query
            logging.info(f"Executing SQL query: {sql_query}")
            results = execute_sql_query(sql_query) # This is synchronous, no await needed here
            logging.info("SQL query execution complete.")
            return results

        except ValueError as ve: # Catch specific ValueError from execute_sql_query for database errors
            logging.error(f"Database execution error: {ve}")
            return {"error": f"Database error: {ve}. Please check your query or data."}
        except Exception as e:
            logging.error(f"An unexpected error occurred in SQLAgent: {e}")
            return {"error": f"An unexpected error occurred while processing your request: {e}"}

# --- END of services/sql_agent.py ---
