from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from dataclasses import dataclass
from mysql.connector import (connection)
import Connection



app = FastAPI()

# templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    #initialize list for websockets connections
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    #accept and append the connection to the list
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    #remove the connection from list
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    #send personal message to the connection
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    #send message to the list of connections
    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.active_connections:
            if(connection == websocket):
                continue
            await connection.send_text(message)

# instance for hndling and dealing with the websocket connections
connectionmanager = ConnectionManager()

# @app.get("/", response_class=HTMLResponse)
# def read_index(request: Request):
#     # Render the HTML template
#     return templates.TemplateResponse("index.html", {"request" : request})

@dataclass
class request_model:
    username:str
    password:str

@app.post("/register")
def register(request:request_model):
    username=request.username
    password=request.password
    #store in mysql with a sno , pk is username and it cant be dup
    # print(username,password)
    Connection.connector("register",username,password)
    print(f"[LOG] User added successfully")

@app.post("/login")
def register(request:request_model):
    username=request.username
    password=request.password
    #check uname and password in sql and validate it and then redirect to the websocket route using their session id if so
    Connection.connector("login",username,password)
    # print(f"[LOG] {res}")
    print("[LOG] User logged in successfully")    


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    #accept connections 
    await connectionmanager.connect(websocket)
    try:
        while True:
            #receive text from the user
            data = await websocket.receive_text()
            await connectionmanager.send_personal_message(f"You : {data}", websocket)
            #broadcast message to the connected user
            await connectionmanager.broadcast(f"Client #{client_id}: {data}", websocket)
            
    #WebSocketDisconnect exception will be raised when client is disconnected
    except WebSocketDisconnect:
        connectionmanager.disconnect(websocket)
        await connectionmanager.broadcast(f"Client #{client_id} left the chat")

# username | password | uniq hash   