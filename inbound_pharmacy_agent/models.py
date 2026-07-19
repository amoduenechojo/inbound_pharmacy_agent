from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class CallStage(Enum):
    START = "start"
    IDENTIFIED = "identified"
    CONVERSING = "conversing"
    ENDED = "ended"


@dataclass
class Pharmacy:

    id: Optional[str]
    name: str
    phone: str
    location: Optional[str] = None
    rx_volume: Optional[int] = None
    is_known: bool = False


@dataclass
class CallSession:

    caller_phone: str
    pharmacy: Optional[Pharmacy] = None
    messages: list = field(default_factory=list)
    stage: CallStage = CallStage.START

    def add_message(self, role: str, content):
        self.messages.append({"role": role, "content": content})
        return None