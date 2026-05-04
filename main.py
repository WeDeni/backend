from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class Task(BaseModel):
    '''Модель задачи'''
    id: str
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    title: str

class Book(BaseModel):
    name: str

book: Book | None = None
tasks: list[Task] = []


@app.get('/tasks', response_model=list[Task])
def get_tasks():
    '''Получить список задач'''
    return tasks


@app.get('/book', response_model=str)
def get_book():
    '''Получить информацию о книге'''
    global book
    name_book = book.name  #type: ignore
    return 'Любимая книга - ' + name_book


@app.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    '''Создать новую задачу'''
    task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(task)
    return task


@app.post('/book', response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: Book):
    '''Создать имя книги'''
    global book
    book = Book(name = payload.name)
    return book