from dataclasses import dataclass
from typing import TypeVar, Generic, List, Protocol 
from angle import AngleDeg360
from robot import Movable, Cleanable, CleaningMode


TRobot = TypeVar('TRobot')
TMovableRobot = TypeVar('TMovableRobot', bound=Movable)
TCleanableRobot = TypeVar('TCleanableRobot', bound=Cleanable)


class Command(Protocol[TRobot]):
    def execute(self, robot: TRobot) -> tuple[str, TRobot]: 
        pass


@dataclass
class MoveCommand(Generic[TMovableRobot]):
    dist: float
    
    def execute(self, robot: TMovableRobot) -> tuple[str, TMovableRobot]:
        return robot.move(self.dist)
        

@dataclass
class TurnCommand(Generic[TMovableRobot]):
    angle: AngleDeg360
    
    def execute(self, robot: TMovableRobot) -> tuple[str, TMovableRobot]:
        return robot.turn(self.angle)
        

@dataclass
class SetStateCommand(Generic[TCleanableRobot]):
    mode: CleaningMode
    
    def execute(self, robot: TCleanableRobot) -> tuple[str, TCleanableRobot]:
        return robot.set_state(self.mode)
        
        
@dataclass
class StartCommand(Generic[TCleanableRobot]):
    
    def execute(self, robot: TCleanableRobot) -> tuple[str, TCleanableRobot]:
        return robot.start()
        
        
@dataclass
class StopCommand(Generic[TCleanableRobot]):
    
    def execute(self, robot: TCleanableRobot) -> tuple[str, TCleanableRobot]:
        return robot.stop()
        
        
class CommandExecutor:
    def execute_all(self, commands: List[Command], robot: Protocol[TRobot]) -> tuple[List[str], Protocol[TRobot]]:
        current_robot = robot
        command_results: List[str] = []
        
        for command in commands:
            status, current_robot = command.execute(current_robot)
            command_results.append(f'status:{status},\n state:\n{current_robot}')
            
        return command_results, current_robot
