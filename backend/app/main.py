import pathlib

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Dummy data storag
PATH_PROMPT_FUNCTION_HUB = pathlib.Path(__file__).parents[1] / "db" / "prompts"

dummy_data = {"juunge/cod/default": "noget data for søren!"}

# ---------------------------------------------------------------------------- #
#                                    Models                                    #
# ---------------------------------------------------------------------------- #


class WritePromptFunctionRequest(BaseModel):
    template: str
    model_args: dict
    auth_token: str
    system_message: str = None
    function_args: dict = None


class ReadPromptFunctionResponse(BaseModel):
    template: str
    model_args: dict
    system_message: str = None
    function_args: dict = None


# ---------------------------------------------------------------------------- #
#                                   Endpoints                                  #
# ---------------------------------------------------------------------------- #


@app.get("/read/")
async def read(
    user: str,
    identifier: str,
    version: str = None,
) -> ReadPromptFunctionResponse:
    if not version:
        version = "default"
    if (PATH_PROMPT_FUNCTION_HUB / user / identifier / version).exists():
        return "Success!"
    else:
        return "Fail.."


@app.post("/write/")
async def write(request: WritePromptFunctionRequest):
    """
    Write data to the dummy data storage based on the provided key and value.
    """

    return {"message": "Data saved successfully", "data": "dummy data"}
