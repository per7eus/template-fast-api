import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routers import user
from .routers import auth
from .database.session import  engine
from .database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(lifespan=lifespan)


app.include_router(user.user_router)
app.include_router(auth.auth_router)


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)