from dataclasses import dataclass, asdict
from typing import Tuple, List

from src.Models.Abstract.base_status import BaseStatus

@dataclass
class AvailableMovesStatus(BaseStatus):
    square: Tuple[int, int]
    description: str = "availble moves"