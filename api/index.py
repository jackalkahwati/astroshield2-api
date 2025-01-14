from fastapi import FastAPI; from mangum import Mangum; app = FastAPI(); handler = Mangum(app, lifespan="off", api_gateway_base_path=None, strip_stage_path=True)
