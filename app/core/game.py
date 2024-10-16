import random
from entities import Board, Player, PlayerType, Property


class Game:
    board: Board
    turn: int = 0
    current_player: Player | None = None

    def __init__(self, board: Board):
        self.board = board

    def __str__(self):
        return f"{self.board.players} - {self.turn}"

    def next_turn(self):
        player_index = self.turn % len(self.board.players)
        self.current_player = self.board.players[player_index]
        self.turn += 1

    @property
    def is_game_over(self) -> bool:
        positive_balance = filter(lambda p: p.balance > 0, self.board.players)
        return len(list(positive_balance)) == 1 or self.turn > 1000


def start_game() -> Game:
    players = [
        Player(300, 0, PlayerType.Impulsive),
        Player(300, 0, PlayerType.Demanding),
        Player(300, 0, PlayerType.Cautious),
        Player(300, 0, PlayerType.Random),
    ]

    random.shuffle(players)

    properties = []

    for _ in range(20):
        price = random.randint(10, 600)
        rent = price * 0.01
        properties.append(Property(price, rent, None))

    game = Game(Board(players=players, properties=properties))

    while not game.is_game_over:
        game.next_turn()

    return game
