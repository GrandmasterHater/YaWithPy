import math
from typing import Self
from angle import AngleDeg360

class Coordinate:
    
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y
        
    def add(self, angle: AngleDeg360, length: float) -> Self:
        angle_rad = angle.get_angle_radians()
        x = self.__x + (length * math.cos(angle_rad))
        y = self.__y + (length * math.sin(angle_rad))
        
        return Coordinate(x, y)
        
    def get_coordinate(self) -> tuple[float, float]:
        return (self.__x, self.__y)
        
    def __str__(self):
        return f'{self.__x:.0f}, {self.__y:.0f}'