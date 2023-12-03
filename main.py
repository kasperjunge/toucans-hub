from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from toucans_hub.db.models import CreatePromptFunction, PromptFunction
from toucans_hub.db.utils import get_session

app = FastAPI()


@app.get("/")
async def home():
    return "Toucans Hub"


@app.post("/prompt-functions/", response_model=PromptFunction)
async def create_prompt(
    prompt_data: CreatePromptFunction,
    session: Session = Depends(get_session),
):
    new_prompt = PromptFunction(**prompt_data.dict())
    try:
        session.add(new_prompt)
        session.commit()
        session.refresh(new_prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_prompt


@app.get("/prompt-functions/{name}", response_model=PromptFunction)
async def read_prompt(
    name: str,
    session: Session = Depends(get_session),
):
    statement = select(PromptFunction).where(PromptFunction.name == name)
    results = session.exec(statement)
    prompt = results.first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
