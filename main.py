from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:3000',
    ],
    allow_methods=['*'],
    allow_headers=['*'],
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


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


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
    for task in tasks:
        if task.title == payload.title:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Задача с таким названием уже существует')
    new_task = Task(id=str(uuid4()), title=payload.title, completed=False)
    tasks.append(new_task)
    return new_task


@app.post('/book', response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: Book):
    '''Создать имя книги'''
    global book
    book = Book(name = payload.name)
    return book

@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdateSchema):
    for task in tasks:
        if task.id == task_id:
            if payload.title:
                task.title = payload.title
            if payload.completed:
                task.completed = payload.completed
            return task

@app.delete('/tasks/{task_id}')
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return