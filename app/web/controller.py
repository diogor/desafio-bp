from app.core.game import start_game
from .response import GameResponse


def game() -> GameResponse:
    new_game = start_game()

    players = sorted(new_game.board.players, key=lambda p: p.balance, reverse=True)

    return GameResponse(
        vencedor=players[0].type.value,
        jogadores=[p.type.value for p in players],
    )
