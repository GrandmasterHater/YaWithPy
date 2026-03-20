from .coordinate import Coordinate
from .angle import AngleDeg360
from .setmode import SetMode

class Robot:
    
    def __init__(self, transfer):
        self.__pos = Coordinate(0.0, 0.0)
        self.__angle = AngleDeg360(0.0)
        self.__mode = SetMode.WATER
        self.__transfer = transfer
        
    def move(self, range: float):
        self.__pos = self.__pos.add(self.__angle, range)
        self.__transfer(f'POS {self.__pos}')
    
    def turn(self, angle: float):
        self.__angle = self.__angle.rotate(angle)
        self.__transfer(f'ANGLE {self.__angle}')
    
    def set(self, mode: SetMode):
        self.__mode = mode
        self.__transfer(f'STATE {self.__mode.value}')
    
    def start(self):
        self.__transfer(f'START WITH {self.__mode.value}')
    
    def stop(self):
        self.__transfer('STOP')