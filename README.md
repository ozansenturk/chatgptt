# chatgptt

both frontend and backend were dockerized. frontend was implemented by react whilst the backend was built by Python FastAPI.
the concept is realtime interaction with chatgpt via websockets. The frontend opens a websocket and starts to communicate with backend. Backend submits incoming messages to the chatgpt to get answers.

set your OPENAI_API_KEY as environment variable before start

docker-compose up --build

localhost:3000 frontend
localhost:8000 backend