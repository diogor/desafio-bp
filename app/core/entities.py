from dataclasses import dataclass
from enum import Enum


class PlayerType(Enum):
    Impulsive = 1
    Demanding = 2
    Cautious = 3
    Random = 4


@dataclass
class Player:
    balance: float
    position: int
    type: PlayerType
    steps: int = 0


@dataclass
class Property:
    price: float
    rent: float
    owner: Player | None


@dataclass
class Board:
    players: list[Player]
    properties: list[Property]
