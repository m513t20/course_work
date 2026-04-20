from dataclasses import dataclass, asdict
from typing import Tuple

from src.Models.Abstract.base_status import BaseStatus

@dataclass
class WrongMoveStatus(BaseStatus):
    initial_square: Tuple[int, int]
    wrong_square: Tuple[int, int]
    description: str = "wrongmove"