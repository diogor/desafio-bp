import random
from app.config.settings import (
    PROPERTY_MAX_PRICE,
    PROPERTY_MIN_PRICE,
    RENT_MAX_PERCENTAGE,
    RENT_MIN_PERCENTAGE,
    TABLE_ROUND_BONUS,
    TURN_LIMIT,
)
from .entities import Board, Player, PlayerType, Property


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

        self._check_player_progress()

        if self.current_player.balance >= 0:
            self._move()
            self._buy_or_rent_property()

        self.turn += 1

    @property
    def is_game_over(self) -> bool:
        positive_balance = filter(lambda p: p.balance > 0, self.board.players)
        return len(list(positive_balance)) == 1 or self.turn > TURN_LIMIT

    def _roll(self) -> int:
        number = random.randint(1, 6)
        self.current_player.steps += number

        if self.current_player.steps > len(self.board.properties):
            self.current_player.steps = 0
            self.current_player.balance += TABLE_ROUND_BONUS

        return number

    def _move(self) -> None:
        spaces = self._roll()
        next_pos = self.current_player.position + spaces
        self.current_player.position = next_pos % len(self.board.properties)

    def _buy_or_rent_property(self) -> None:
        player_type = self.current_player.type
        property = self.board.properties[self.current_player.position]

        if property.owner is None:
            match player_type:
                case PlayerType.Impulsive:
                    self._buy_property()
                case PlayerType.Demanding:
                    if property.rent > 50:
                        self._buy_property()
                case PlayerType.Cautious:
                    if self.current_player.balance - property.price >= 80:
                        self._buy_property()
                case PlayerType.Random:
                    if random.choice([True, False]):
                        self._buy_property()

        if property.owner:
            self._rent_property()

    def _buy_property(self) -> None:
        property = self.board.properties[self.current_player.position]

        if self.current_player.balance < property.price:
            return

        self.current_player.balance -= property.price
        property.owner = self.current_player

    def _rent_property(self) -> None:
        property = self.board.properties[self.current_player.position]

        if not property.owner or property.owner == self.current_player:
            return

        self.current_player.balance -= property.rent
        property.owner.balance += property.rent

    def _check_player_progress(self) -> None:
        player = self.current_player

        if player.balance < 0:
            owned_properties = filter(
                lambda p: p.owner == player, self.board.properties
            )

            for property in owned_properties:
                property.owner = None


def start_game() -> Game:
    players = [
        Player(300, 0, PlayerType.Impulsive),
        Player(300, 0, PlayerType.Demanding),
        Player(300, 0, PlayerType.Cautious),
        Player(300, 0, PlayerType.Random),
    ]

    random.shuffle(players)

    for i, player in enumerate(players):
        player.play_order = i
        player.position = -1

    properties = []

    for _ in range(20):
        price = random.randint(PROPERTY_MIN_PRICE, PROPERTY_MAX_PRICE)
        rent = round(
            random.uniform(
                price * (RENT_MIN_PERCENTAGE / 100), price * (RENT_MAX_PERCENTAGE / 100)
            ),
            2,
        )
        properties.append(Property(price, rent, None))

    game = Game(Board(players=players, properties=properties))

    while not game.is_game_over:
        game.next_turn()

    return game
