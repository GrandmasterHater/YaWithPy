from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, UTC

REQUESTS = "requests"
RESULTS  = "results"

@dataclass
class Event(ABC):
    version: int
    occurred_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    
### Requested Events

@dataclass
class MoveRequestedEvent(Event):
    dist: int = 0


@dataclass
class TurnRequestedEvent(Event):
    angle: int = 0
    
    
@dataclass   
class SetModeRequestedEvent(Event):
    mode: str = ''
    
    
@dataclass
class StartRequestedEvent(Event):
    pass
    
@dataclass
class StopRequestedEvent(Event):
   pass
   
   
   
### Robot action events

@dataclass
class MovedEvent(Event):
    x: int = 0
    y: int = 0


@dataclass
class TurnedEvent(Event):
    angle: int = 0
    
    
@dataclass   
class SetModeEvent(Event):
    mode: str = ''
    
    
@dataclass
class StartedEvent(Event):
    pass
    
@dataclass
class StopedEvent(Event):
   pass
   
