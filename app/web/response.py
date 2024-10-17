from pydantic import BaseModel


class GameResponse(BaseModel):
    vencedor: str
    jogadores: list[str]
