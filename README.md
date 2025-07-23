# llmsqlpostgres

#steps:
1.set up virtual environment
2.pip install -r requirements.txt
3.setup your api key in .env file, DATABASE_URL and GOOGLE_API_KEY.
4.Run this command in terminal to start the app "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
5.Then run index.html file , opne using liver server

#run this in cmd
curl -X POST "http://localhost:8000/api/chat" ^
-H "Content-Type: application/json" ^
-d "{\"message\": \"Show me all users\"}" <-- add your query here 

