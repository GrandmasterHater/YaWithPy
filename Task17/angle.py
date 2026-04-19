import math
from typing import Self

class AngleDeg360:
    FULL_CIRCLE_DEG: float = 360.0
    
    def __init__(self, angle: float):
        self.__angle = angle % self.FULL_CIRCLE_DEG
        
    def rotate(self, turn_on_angle: Self) -> Self:
        new_angle  = (self.__angle + turn_on_angle.__angle) % self.FULL_CIRCLE_DEG
        return AngleDeg360(new_angle)
        
    def get_angle(self) -> float:
        return self.__angle
        
    def get_angle_radians(self) -> float:
        return math.radians(self.__angle)
        
    def __str__(self):
        return f'{self.__angle:.0f} deg.'
        