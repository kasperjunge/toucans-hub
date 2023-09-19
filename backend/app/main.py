import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Constants
PATH_PROMPT_FUNCTION_HUB = Path(__file__).parents[1] / "db" / "prompts"
DEFAULT_VERSION = "default"


# Models
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


# Endpoints
@app.get("/read/")
async def read(
    user: str, identifier: str, version: str = DEFAULT_VERSION
) -> ReadPromptFunctionResponse:
    path = PATH_PROMPT_FUNCTION_HUB / user / identifier / version

    if not path.exists():
        raise HTTPException(status_code=404, detail="Data not found.")

    # Load template
    with open(path / "template.txt", "r") as f:
        template = f.read()

    # Load model args
    with open(path / "model_args.json", "r") as f:
        model_args = json.load(f)

    # Load system message
    system_message_path = path / "system_message.txt"
    system_message = (
        system_message_path.read_text() if system_message_path.exists() else None
    )

    # Load function calling args
    function_args_path = path / "function_args.json"
    function_args = (
        json.load(function_args_path.open()) if function_args_path.exists() else None
    )

    return ReadPromptFunctionResponse(
        template=template,
        model_args=model_args,
        system_message=system_message,
        function_args=function_args,
    )


@app.post("/write/")
async def write(request: WritePromptFunctionRequest) -> dict:
    user, identifier, version = request.template.split("/")
    if not version:
        version = DEFAULT_VERSION

    path = PATH_PROMPT_FUNCTION_HUB / user / identifier / version
    path.mkdir(parents=True, exist_ok=True)  # Ensure directories exist

    # Save template
    with open(path / "template.txt", "w") as f:
        f.write(request.template)

    # Save model args
    with open(path / "model_args.json", "w") as f:
        json.dump(request.model_args, f)

    # Save system message if provided
    if request.system_message:
        with open(path / "system_message.txt", "w") as f:
            f.write(request.system_message)

    # Save function calling args if provided
    if request.function_args:
        with open(path / "function_args.json", "w") as f:
            json.dump(request.function_args, f)

    return {"status": "success"}
