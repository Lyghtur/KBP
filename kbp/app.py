
from fastapi import FastAPI
from kbp.middlewares import add_middlewares, database_connection, fs_connection
from kbp.routes import router

app = FastAPI()


add_middlewares(app, database_connection, fs_connection)


app.include_router(router)
