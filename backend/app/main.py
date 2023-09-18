from fastapi import FastAPI

app = FastAPI()

# Dummy data storage
dummy_data = {}


@app.get("/read/{key}")
async def read(key: str):
    """
    Read data from the dummy data storage based on the provided key.
    """
    if key in dummy_data:
        return {"message": "Data retrieved successfully", "data": dummy_data[key]}
    else:
        return {"message": "Data not found", "data": None}


@app.post("/write/{key}")
async def write(key: str, value: str):
    """
    Write data to the dummy data storage based on the provided key and value.
    """
    dummy_data[key] = value
    return {"message": "Data saved successfully", "data": {key: value}}
