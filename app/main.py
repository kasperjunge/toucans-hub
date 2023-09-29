from fastapi import FastAPI

app = FastAPI()


# Endpoints
@app.get("//")
async def home():
    return "Toucans Hub"
