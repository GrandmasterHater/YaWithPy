from abc import ABC, abstractmethod
from typing import Callable, List
from dataclasses import dataclass
from collections import namedtuple
from enum import StrEnum
import math


RobotState = namedtuple("RobotState", "x y angle mode")

class Mode(StrEnum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

@dataclass
class Responce(ABC):
    robot_state: RobotState
    is_success: bool
    
    
@dataclass 
class MoveResponce(Responce):
    dist: float
    
@dataclass 
class TurnResponce(Responce):
    angle: float
    
@dataclass 
class SetStateResponce(Responce):
    state: float
    
@dataclass 
class StartResponce(Responce):
    pass
    
@dataclass 
class StopResponce(Responce):
    pass
    
    
class AstCommandNode(ABC):
    @abstractmethod
    def interpret(self, state: RobotState) -> Responce:
        pass

@dataclass
class NotTerminalNode(AstCommandNode):
    f_next: Callable[[Responce], AstCommandNode]
    
    
@dataclass
class MoveNode(NotTerminalNode):
    dist: float
    
    def interpret(self, state: RobotState) -> Responce:
        angle_rads = state.angle * (math.pi/180.0)
        
        new_state = RobotState(
            state.x + self.dist * math.cos(angle_rads),
            state.y + self.dist * math.sin(angle_rads),
            state.angle,
            state.mode)
        return MoveResponce(new_state, True, self.dist)
    
@dataclass
class TurnNode(NotTerminalNode):
    angle: float
    
    def interpret(self, state: RobotState) -> Responce:
        new_state = RobotState(
            state.x,
            state.y,
            state.angle + self.angle,
            state.mode)
        return TurnResponce(new_state, True, self.angle)
    
@dataclass
class SetStateNode(NotTerminalNode):
    mode: Mode
    
    def interpret(self, state: RobotState) -> Responce:
        new_state = RobotState(
            state.x,
            state.y,
            state.angle,
            self.mode)
        return SetStateResponce(new_state, True, self.mode)
    
@dataclass
class StartNode(NotTerminalNode):
    
    def interpret(self, state: RobotState) -> Responce:
        return StartResponce(state, True)
    
@dataclass
class StopNode(AstCommandNode):
    
    def interpret(self, state: RobotState) -> Responce:
        return StopResponce(state, True)
        
        
def interpret_node(node: AstCommandNode, state: RobotState, responces_log: List[Responce]):
    
    responce = node.interpret(state)
    responces_log.append(responce)
    
    if isinstance(node, StopNode):
        return
    
    next_node = node.f_next(responce)
    interpret_node(next_node, responce.robot_state, responces_log)
    

start_state = RobotState(0.0, 0.0, 0, Mode.WATER)
responces_log: List[Responce] = []

f_stop = lambda responce: StopNode()
f_move_50 = lambda responce: MoveNode(f_stop, 50)
f_start = lambda responce: StartNode(f_move_50)
f_set_state = lambda responce: SetStateNode(f_start, Mode.SOAP)
f_turn = lambda responce: TurnNode(f_set_state, -90)
move_node = MoveNode(f_turn, 100)

interpret_node(move_node, start_state, responces_log)

for responce in responces_log:
    print(responce)
