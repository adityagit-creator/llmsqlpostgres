
# 🧠 LLM SQL Chatbot for PostgreSQL

This project allows you to **query your PostgreSQL database using natural language**. It's powered by **Google Gemini** and built using **FastAPI** on the backend and a minimal **Tailwind CSS** frontend.

---

## 📦 Setup Steps

1. **Set up a virtual environment**  
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate  # On Linux/Mac
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure `.env` file**  
   Create a `.env` file in the root folder with:
   ```dotenv
   DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database>
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Run the backend API server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open the frontend**
   - Use **Live Server** extension in VSCode or open `index.html` manually in the browser.
   - Type your question like:  
     `"Show me all users"` or `"Which products cost more than 50?"`

---

## 📡 Test API using `curl` (CMD)

```bash
curl -X POST "http://localhost:8000/api/chat" ^
-H "Content-Type: application/json" ^
-d "{\"message\": \"Show me all users\"}"
```

Replace the message with your custom natural language query.

---

## 🖼️ Output Display Options
  ![Output](https://github.com/adityagit-creator/llmsqlpostgres/blob/main/Screenshot%202025-07-23%20184442.png)
## 🛡️ Allowed Queries

✅ Supported SQL operations:
- `SELECT`, `INSERT`, `UPDATE`, `DELETE`

❌ Disallowed for safety:
- `CREATE`, `DROP`, `ALTER`, `TRUNCATE`, etc.

---

## 🧪 Example Queries

- **"Show me all users"**
- **"Count products where price > 100"**
- **"Add a new user with name John"**
- **"Delete the product with id 3"**

---
