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
    existing_prompt = (
        session.query(PromptFunction)
        .filter_by(hash_id=prompt_data.hash_id, name=prompt_data.name)
        .first()
    )

    if existing_prompt:
        return existing_prompt

    new_prompt = PromptFunction(**prompt_data.dict())
    session.add(new_prompt)
    session.commit()
    session.refresh(new_prompt)

    return new_prompt


@app.get("/prompt-functions/{function_name}", response_model=PromptFunction)
async def read_prompt(
    function_name: str,
    session: Session = Depends(get_session),
):
    statement = (
        select(PromptFunction)
        .where(PromptFunction.name == function_name)
        .order_by(PromptFunction.created_at.desc())
    )
    results = session.exec(statement)
    prompt = results.first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt function not found")
    return prompt


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
