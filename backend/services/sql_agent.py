from backend.services.llm_service import LLMService
from backend.database.connection import execute_sql_query
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SQLAgent:
    def __init__(self):
        self.llm_service = LLMService()
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
        sql_query = llm_response.strip()
        if not sql_query or sql_query == "INVALID_QUERY":
            logging.warning("LLM returned an empty or 'INVALID_QUERY' response.")
            return "INVALID_QUERY"
        allowed_dml_keywords = r'^\s*(SELECT|INSERT|UPDATE|DELETE)\b'
        disallowed_keywords = r'\b(CREATE|ALTER|DROP|TRUNCATE|GRANT|REVOKE|VACUUM|REINDEX|REFRESH)\b'
        if not re.match(allowed_dml_keywords, sql_query, re.IGNORECASE):
            logging.warning(f"Generated SQL does not start with an allowed DML keyword: {sql_query}")
            return "UNSAFE_QUERY"
        if re.search(disallowed_keywords, sql_query, re.IGNORECASE):
            logging.warning(f"Generated SQL contains disallowed keywords: {sql_query}")
            return "UNSAFE_QUERY"
        if ';' in sql_query.strip(' ;') and sql_query.strip().count(';') > 1:
            logging.warning(f"Generated SQL contains multiple statements: {sql_query}")
            return "UNSAFE_QUERY"

        return sql_query

    async def process_query(self, natural_language_query: str): 
        try:
            full_prompt = f"{self.system_prompt}\nUser: \"{natural_language_query}\"\nSQL:"
            logging.info(f"Sending prompt to LLM: {full_prompt}")
            llm_raw_response = await self.llm_service.generate_text(full_prompt) 
            sql_query = self._extract_sql_from_llm_response(llm_raw_response)
            logging.info(f"LLM generated SQL: {sql_query}")

            if sql_query == "INVALID_QUERY":
                return {"error": "Could not generate a valid SQL query from your request. Please rephrase or provide more context."}
            elif sql_query == "UNSAFE_QUERY":
                return {"error": "Generated query contains disallowed operations. Only SELECT, INSERT, UPDATE, and DELETE are permitted."}
            logging.info(f"Executing SQL query: {sql_query}")
            results = execute_sql_query(sql_query)
            logging.info("SQL query execution complete.")
            return results

        except ValueError as ve: 
            logging.error(f"Database execution error: {ve}")
            return {"error": f"Database error: {ve}. Please check your query or data."}
        except Exception as e:
            logging.error(f"An unexpected error occurred in SQLAgent: {e}")
            return {"error": f"An unexpected error occurred while processing your request: {e}"}
