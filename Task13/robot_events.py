from typing import Protocol
from datetime import datetime, UTC
from dataclasses import dataclass, field


class RobotEvent(Protocol):
    version: int
    occurred_time: datetime
    
    
@dataclass
class MoveEvent:
    version: int
    x: int
    y: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class TurnEvent:
    version: int
    angle: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    
@dataclass   
class SetModeEvent:
    version: int
    mode: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    
@dataclass
class StartEvent:
    version: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    
    
@dataclass
class StopEvent:
    version: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))
