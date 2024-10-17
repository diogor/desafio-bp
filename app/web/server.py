from fastapi import FastAPI
from .response import GameResponse
from .controller import game

app = FastAPI()


@app.get("/jogo/simular", response_model=GameResponse)
async def jogo() -> GameResponse:
    return game()
