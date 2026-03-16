from enum import StrEnum
import math
from typing import Self, List
import argparse

class SetMode(StrEnum):
    NONE = ''
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class AngleDeg360():
    
    def __init__(self, start_angle: float):
        self.__angle = start_angle
        
    def rotate(self, angle: float):
        self.__angle = (self.__angle + angle) % 360.0
        
    def get_angle(self) -> float:
        return self.__angle
        
    def __str__(self):
        return f'{self.__angle:.0f}'
        
class Vector2():
    
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y
        
    def add(self, angle: AngleDeg360, length: float) -> Self:
        angle_rad = math.radians(angle)
        x = self.__x + (length * math.cos(angle_rad))
        y = self.__y + (length * math.sin(angle_rad))
        
        return Vector2(x, y)
        
    def __str__(self):
        return f'{self.__x:.0f}, {self.__y:.0f}'


class Robot:
    
    def __init__(self):
        self.__pos = Vector2(0.0, 0.0)
        self.__angle = AngleDeg360(0.0)
        self.__is_started = False
        self.__mode = SetMode.NONE
        
    def move(self, range: float):
        angle = self.__angle.get_angle()
        self.__pos = self.__pos.add(angle, range)
        print(f'POS {self.__pos}')
    
    def turn(self, angle: float):
        self.__angle.rotate(angle)
        print(f'ANGLE {self.__angle}')
    
    def set(self, mode: SetMode):
        self.__mode = mode
        print(f'STATE {self.__mode.name}')
    
    def start(self):
        self.__is_started = True
        print(f'START WITH {self.__mode.name}')
    
    def stop(self):
        self.__is_started = False
        print('STOP')
        

def initiate(commandsRaw: List[str], robot: Robot):
    for commandRaw in commandsRaw:
        HandleCommand(commandRaw, robot)
        
def HandleCommand(commandRaw: str, robot: Robot):
    COMMAND_INDEX = 0
    COMMAND_ARG_INDEX = 1
    
    params = commandRaw.split(' ')
        
    match params[COMMAND_INDEX].lower():
        case 'move':
            robot.move(float(params[COMMAND_ARG_INDEX]))
        case 'turn':
            robot.turn(float(params[COMMAND_ARG_INDEX]))
        case 'set':
            robot.set(SetMode(params[COMMAND_ARG_INDEX]))
        case 'start':
            robot.start()
        case 'stop':
            robot.stop()
        case _:
            print('Unexpected command!')
            
   
commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop']  

robot = Robot()

initiate(commands, robot)
