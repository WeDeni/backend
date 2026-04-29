from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_base_page():
    return {'message': 'Hello World!'}