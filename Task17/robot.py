from dataclasses import dataclass
from enum import StrEnum
from coordinate import Coordinate
from angle import AngleDeg360
from typing import Self, Protocol


class CleaningMode(StrEnum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"
    
    
class Movable(Protocol):
    def move(self, dist: float) -> tuple[str, Self]:
        pass
    
    def turn(self, angle: AngleDeg360) -> tuple[str, Self]:
        pass
    

class Cleanable(Protocol):
    def set_state(self, mode: CleaningMode) -> tuple[str, Self]:
        pass
    
    def start(self) -> tuple[str, Self]:
        pass
    
    def stop(self) -> tuple[str, Self]:
        pass
    
    
@dataclass
class RobotCleaner:
    coordinate: Coordinate
    angle: AngleDeg360
    mode: CleaningMode
    
    def move(self, dist: float) -> tuple[str, Self]:
        new_coordinate = self.coordinate.add(self.angle, dist)
        
        new_robot = RobotCleaner(
            new_coordinate,
            self.angle,
            self.mode)
            
        return "Ok", new_robot
        
    def turn(self, angle: AngleDeg360) -> tuple[str, Self]:
        new_angle = self.angle.rotate(angle)
        
        new_robot = RobotCleaner(
            self.coordinate,
            new_angle,
            self.mode)
            
        return "Ok", new_robot
        
    def set_state(self, mode: CleaningMode) -> tuple[str, Self]:
        new_robot = RobotCleaner(
            self.coordinate,
            self.angle,
            mode)
            
        return "Ok", new_robot
        
    def start(self) -> tuple[str, Self]:
        return "Ok", RobotCleaner(
            self.coordinate,
            self.angle,
            self.mode)
        
    def stop(self) -> tuple[str, Self]:
        return "Ok", RobotCleaner(
            self.coordinate,
            self.angle,
            self.mode)
            
    def __str__(self):
        return ( f'coordinate: {self.coordinate},\n'
                 f'angle: {self.angle},\n'
                 f'mode: {self.mode}')
        