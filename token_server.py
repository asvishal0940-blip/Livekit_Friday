import os
from fastapi import FastAPI
from livekit import api
from dotenv import load_dotenv
import uuid

load_dotenv()

app = FastAPI()

@app.get("/token")
async def get_token():
    # Load credentials from your .env file
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    # Generate a unique identity for the participant
    participant_identity = f"android_user_{uuid.uuid4().hex[:6]}"

    # Create the token
    token = api.AccessToken(api_key, api_secret) \
        .with_identity(participant_identity) \
        .with_name("Friday User") \
        .with_grants(api.VideoGrants(
            room_join=True,
            room="default-room", # Ensure this matches your agent's room
        ))

    return {
        "server_url": url,
        "participant_token": token.to_jwt()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
