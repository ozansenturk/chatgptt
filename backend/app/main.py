import os
import logging
from openai import RateLimitError
from openai import AsyncOpenAI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger()

# Load OpenAI API key from environment
load_dotenv()

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Managing active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# ChatGPT interaction function
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
async def get_chatgpt_response(user_message: str) -> str:
    try:
        client = AsyncOpenAI()
        completion = await client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": user_message}])

        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": user_message}],
        # )
        chatgpt_reply = completion.choices[0].message['content'].strip()
        return chatgpt_reply
    except RateLimitError:
        # Raising error to trigger retry
        logger.error("retrying...")
        raise
    except Exception as e:
        # Raise other errors to handle them in the route function
        logger.critical("another exception")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for chat communication
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast user message to all clients
            await manager.broadcast(f"User says: {data}")

            # Get response from ChatGPT
            chatgpt_reply = await get_chatgpt_response(data)
            # Broadcast ChatGPT's response to all clients
            await manager.broadcast(f"ChatGPT says: {chatgpt_reply}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A user has left the chat.")