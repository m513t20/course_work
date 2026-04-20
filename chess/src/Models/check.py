from dataclasses import dataclass, asdict
from typing import Tuple

from src.Models.Abstract.base_status import BaseStatus

@dataclass
class CheckStatus(BaseStatus):
    square: Tuple[int, int]
    description: str = "check"