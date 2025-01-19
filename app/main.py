from fastapi import FastAPI

from app.api.bitmex.main import router as bitmex

app = FastAPI()
app.include_router(bitmex)


@app.get("/")
async def root():
    return {"message": "Hello World"}