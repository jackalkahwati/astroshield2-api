from fastapi import FastAPI; from mangum import Mangum; app = FastAPI(); @app.get("/"); async def root(): return {"message": "Hello from AstroShield"}; handler = Mangum(app)
