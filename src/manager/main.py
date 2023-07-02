from fastapi import FastAPI

from manager.controllers.status import status_router


app = FastAPI()
app.include_router(status_router)