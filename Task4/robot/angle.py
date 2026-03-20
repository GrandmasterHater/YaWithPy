import math
from typing import Self

class AngleDeg360:
    
    def __init__(self, angle: float):
        self.__angle = angle
        
    def rotate(self, angle: float) -> Self:
        new_angle  = (self.__angle + angle) % 360.0
        return AngleDeg360(new_angle)
        
    def get_angle(self) -> float:
        return self.__angle
        
    def get_angle_radians(self) -> float:
        return math.radians(self.__angle)
        
    def __str__(self):
        return f'{self.__angle:.0f}'