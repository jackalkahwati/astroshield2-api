from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from AstroShield"}

handler = Mangum(app, lifespan="off")
