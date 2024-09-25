import datetime
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

from models import Event
# Load environment variables from a .env file
load_dotenv()

# Initialize Supabase client using the URL and key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Initialize an empty list to hold events
events = []

# Function to load all events from the Supabase database into the events list
def load_all_events():
    try:
        # Execute the query to select all events from the 'events' table
        response = supabase.table('events').select("*").execute()
        # Check if the query was successful and data was retrieved
        if response.data is not None:
            print("Events retrieved successfully:")
            for event in response.data:
                events.append(event)  # Append each event to the events list
        else:
            print("No events found or an error occurred.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print any error that occurs during the query

# Load all events from the database when the application starts
load_all_events()

# Initialize the FastAPI app
app = FastAPI()

# Define the origins allowed for CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost",
    "http://localhost:5173",
]

# Add CORS middleware to the FastAPI app to allow requests from specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials like cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to create a new event
@app.post('/events/', response_model=Event, status_code=201)
def create_event(event: Event):
    # Prepare the event data to be inserted into the database
    event_data = {
        "date": str(datetime.datetime.today()),  # Current date as the event date
        "title": event.title,
        "description": event.description
    }

    try:
        # Insert the event data into the 'events' table in the Supabase database
        supabase.table("events").insert(event_data).execute()

        # Reload the events list with the updated data
        global events
        events = []  # Clear the events list
        load_all_events()  # Load updated events from the database
        return event  # Return the created event as a response
    except Exception as e:
        return f"An error occurred {str(e)}"  # Return an error message if insertion fails

# Endpoint to retrieve all events from the events list
@app.get('/events/')
def get_all_events():
    return events  # Return the list of events

# Endpoint to retrieve a single event using its ID
@app.get('/events/{event_id}/')
def get_event(event_id: int, response: Response):
    event = None

    # Search for the event with the given event_id in the events list
    for ev in events:
        if ev['id'] == event_id:
            event = ev
            break

    # If the event is not found, return a 404 error
    if event is None:
        response.status_code = 404
        return 'Event not found'

    # Return the event details if found
    return event

# Endpoint to update an event with the specified ID
@app.put('/events/{event_id}/')
def update_event(event_id: int, title: Optional[str] = None,
                 date: Optional[str] = None, description: Optional[str] = None):

    update_data = {}  # Dictionary to hold the fields to be updated

    # Add fields to the update_data dictionary only if they are provided
    if title:
        update_data["title"] = title
    if date:
        update_data["date"] = date
    if description:
        update_data["description"] = description

    # Update the 'updated_at' timestamp to the current time
    update_data["updated_at"] = datetime.datetime.utcnow().isoformat()

    # Update the event data in the database using the provided event_id
    supabase.table("events").update(update_data).eq("id", event_id).execute()

    # Reload the events list with the updated data
    global events
    events = []  # Clear the events list
    load_all_events()  # Load updated events from the database
    return update_data  # Return the updated data as a response
