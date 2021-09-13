from fastapi import FastAPI
import routers

app = FastAPI(title='Auth server')

app.include_router(routers.router)
