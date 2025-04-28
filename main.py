import os
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory=Path.cwd() / "static"), name="static")

# Templates
templates = Jinja2Templates(directory=Path.cwd() / "templates")

# mongo storage for todos
mongo_client = AsyncIOMotorClient(os.getenv("MONGO_CONNECTION_STRING"))
db = mongo_client["todos"]
todos_collection = db["todos"]


async def get_todos():
    return await todos_collection.find().to_list(length=100)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, todos: list = Depends(get_todos)):
    print(todos)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.post("/todos")
async def add_todo(request: Request):
    form_data = await request.form()
    todo_text = form_data.get("todo")
    if todo_text:
        await todos_collection.insert_one({"text": todo_text, "completed": False})
    return templates.TemplateResponse("todos.html", {"request": request, "todos": await get_todos()})


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str, request: Request):
    await todos_collection.delete_one({"_id": ObjectId(todo_id)})
    return templates.TemplateResponse("todos.html", {"request": request, "todos": await get_todos()})


@app.put("/todos/{todo_id}")
async def toggle_todo(todo_id: str, request: Request):
    todo = await todos_collection.find_one({"_id": ObjectId(todo_id)})
    result = await todos_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": {"completed": not todo["completed"]}},
    )
    print(result)
    return templates.TemplateResponse("todos.html", {"request": request, "todos": await get_todos()})
