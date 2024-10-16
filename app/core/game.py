import random
from entities import Board, Player, PlayerType, Property


class Game:
    board: Board
    turn: int = 0
    current_player: Player

    def __init__(self, board: Board):
        self.board = board

    def __str__(self):
        return f"{self.board.players} - {self.turn}"

    def next_turn(self):
        player_index = self.turn % len(self.board.players)
        self.current_player = self.board.players[player_index]

        self._move(self._roll())
        self._operate()

        self.turn += 1

    @property
    def is_game_over(self) -> bool:
        positive_balance = filter(lambda p: p.balance > 0, self.board.players)
        return len(list(positive_balance)) == 1 or self.turn > 1000

    def _roll(self) -> int:
        return random.randint(1, 6)

    def _move(self, spaces: int) -> None:
        next_pos = self.current_player.position + spaces
        self.current_player.position = next_pos % len(self.board.properties)

    def _operate(self) -> None:
        player_type = self.current_player.type
        property = self.board.properties[self.current_player.position]

        match player_type:
            case PlayerType.Impulsive:
                self._negotiate_property()
            case PlayerType.Demanding:
                if property.rent > 50:
                    self._negotiate_property()
            case PlayerType.Cautious:
                if self.current_player.balance - property.price >= 80:
                    self._negotiate_property()
            case PlayerType.Random:
                if random.choice([True, False]):
                    self._negotiate_property()

    def _negotiate_property(self) -> None:
        property = self.board.properties[self.current_player.position]

        if self.current_player.balance < property.price:
            return

        self.current_player.balance -= property.price
        property.owner = self.current_player


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
