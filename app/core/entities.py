from dataclasses import dataclass
from enum import Enum


class PlayerType(Enum):
    Impulsive = "impulsivo"
    Demanding = "exigente"
    Cautious = "cauteloso"
    Random = "aleatório"


@dataclass
class Player:
    balance: float
    position: int
    type: PlayerType
    steps: int = 0
    play_order: int = 0


@dataclass
class Property:
    price: float
    rent: float
    owner: Player | None


@dataclass
class Board:
    players: list[Player]
    properties: list[Property]
