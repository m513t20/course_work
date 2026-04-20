from dataclasses import dataclass, asdict
from typing import Tuple, List

from src.Models.Abstract.base_status import BaseStatus

@dataclass
class MateStatus(BaseStatus):
    atacking_squares: Tuple[int, int]
    description: str = "mate"