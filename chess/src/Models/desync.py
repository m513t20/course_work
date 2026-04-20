import chess

from dataclasses import dataclass, asdict
from typing import Tuple, List

from src.Models.Abstract.base_status import BaseStatus

@dataclass
class DesyncStatus(BaseStatus):
    Square: Tuple[int, int]
    figure: chess.PieceType
    description: str = "desync"