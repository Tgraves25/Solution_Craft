import openai
import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from django.apps import AppConfig

# Django App Config
class SolutionCraftAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solution_craft_app'

# FastAPI application setup
app = FastAPI()

# CORS configuration
origins = [
    "http://127.0.0.1:3000",  
    "http://localhost:3000"    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY") 



# Example: Login route for authentication
@app.post("/api/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "test" and form_data.password == "test":
        return {"access_token": "fake_token", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Example: Route to get ticket details
@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    return {"ticket_id": ticket_id, "status": "open", "description": "This is a ticket."}

# Example: Route to create a new ticket (POST request)
@app.post("/api/tickets/")
async def create_ticket(title: str, description: str, priority: str):
    return {"message": "Ticket created", "title": title, "description": description, "priority": priority}

# Example: Route to list all tickets
@app.get("/api/tickets/")
async def list_tickets():
    return [{"ticket_id": 1, "status": "open", "description": "First ticket."},
            {"ticket_id": 2, "status": "closed", "description": "Second ticket."}]

# AI Recommendation Route
@app.get("/api/ai_recommendation/{ticket_id}")
async def get_ai_recommendation(ticket_id: int):

    ticket_description = "Customer is having trouble logging into their account. They keep getting an error message."
    
    try:
        # OpenAI API call to generate a recommendation
        response = openai.Completion.create(
            engine="text-davinci-003", 
            prompt=f"Ticket description: {ticket_description}\nProvide a relevant recommendation or solution for this issue:",
            max_tokens=150,
            temperature=0.7,
        )
        
        recommendation = response.choices[0].text.strip()
        return {"recommendation": recommendation}

    except Exception as e:
        return {"error": str(e)}, 500
