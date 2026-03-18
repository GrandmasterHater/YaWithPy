from enum import StrEnum, Enum
import math
from typing import Self, List
import argparse

class SetMode(StrEnum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class AngleDeg360:
    
    def __init__(self, angle: float):
        self.__angle = angle
        
    def rotate(self, angle: float):
        new_angle  = (self.__angle + angle) % 360.0
        return AngleDeg360(new_angle)
        
    def get_angle(self) -> float:
        return self.__angle
        
    def get_angle_radians(self) -> float:
        return math.radians(self.__angle)
        
    def __str__(self):
        return f'{self.__angle:.0f}'
        
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


class Robot:
    
    def __init__(self):
        self.__pos = Coordinate(0.0, 0.0)
        self.__angle = AngleDeg360(0.0)
        self.__mode = SetMode.WATER
        
    def move(self, range: float):
        self.__pos = self.__pos.add(self.__angle, range)
        print(f'POS {self.__pos}')
    
    def turn(self, angle: float):
        self.__angle = self.__angle.rotate(angle)
        print(f'ANGLE {self.__angle}')
    
    def set(self, mode: SetMode):
        self.__mode = mode
        print(f'STATE {self.__mode.value}')
    
    def start(self):
        print(f'START WITH {self.__mode.value}')
    
    def stop(self):
        print('STOP')
        
        
class InterpretStatus(Enum):
    OK = 0
    UNEXPECTED_COMMAND = 1
    INVALID_COMMAND_ARGUMENT = 2
    MISSING_COMMAND_ARGUMENT = 3

# В идеале конечно нужно разделить логику интерпретатора на парсер, фабрику команд и команду, но для такой задачи как-будто кажется избыточным.
class CommandsInterpreter:
    COMMAND_INDEX = 0
    COMMAND_ARG_INDEX = 1
    
    def __init__(self, robot: Robot):
        self.__robot = robot
    
    def interpret(self, commands: list[str]) -> InterpretStatus:
        status = None
        
        for command in commands:
            status = self.__handle_command(command, self.__robot)
            
            if (status != InterpretStatus.OK):
                break
            
        return status
       
    def __is_valid_command_length(self, command: List[str], expected_length: int) -> bool:
        return len(command) == expected_length
            
    def __execute_move_command(self, command: List[str], robot: Robot) -> InterpretStatus:
        length = None
        COMMAND_LEN_WITH_ARGUMENTS = 2
        
        if (not self.__is_valid_command_length(command, COMMAND_LEN_WITH_ARGUMENTS)):
            return InterpretStatus.MISSING_COMMAND_ARGUMENT
        
        try:
            length = float(command[self.COMMAND_ARG_INDEX])
        except (ValueError, TypeError):
            return InterpretStatus.INVALID_COMMAND_ARGUMENT
        
        robot.move(length)   
        return InterpretStatus.OK
         
    def __execute_turn_command(self, command: list[str], robot: Robot) -> InterpretStatus:
        angle = None
        COMMAND_LEN_WITH_ARGUMENTS = 2
        
        if (not self.__is_valid_command_length(command, COMMAND_LEN_WITH_ARGUMENTS)):
            return InterpretStatus.MISSING_COMMAND_ARGUMENT
        
        try:
            angle = float(command[self.COMMAND_ARG_INDEX])
        except (ValueError, TypeError):
            return InterpretStatus.INVALID_COMMAND_ARGUMENT
        
        robot.turn(angle)   
        return InterpretStatus.OK
         
    def __execute_set_command(self, command: list[str], robot: Robot) -> InterpretStatus:
        mode = None
        COMMAND_LEN_WITH_ARGUMENTS = 2
        
        if (not self.__is_valid_command_length(command, COMMAND_LEN_WITH_ARGUMENTS)):
            return InterpretStatus.MISSING_COMMAND_ARGUMENT
        
        try:
            mode = SetMode(command[self.COMMAND_ARG_INDEX])
        except (ValueError, TypeError):
            return InterpretStatus.INVALID_COMMAND_ARGUMENT
        
        robot.set(mode)   
        return InterpretStatus.OK
         
    def __execute_start_command(self, command: list[str], robot: Robot) -> InterpretStatus:
         robot.start()   
         return InterpretStatus.OK
         
    def __execute_stop_command(self, command: list[str], robot: Robot) -> InterpretStatus:
         robot.stop()   
         return InterpretStatus.OK
        
    
    def __handle_command(self, commandRaw: str, robot: Robot) -> InterpretStatus:
    
        command = commandRaw.split(' ')
        
        match command[self.COMMAND_INDEX].lower():
            case 'move':
                return self.__execute_move_command(command, robot)
            case 'turn':
                return self.__execute_turn_command(command, robot)
            case 'set':
                return self.__execute_set_command(command, robot)
            case 'start':
                return self.__execute_start_command(command, robot)
            case 'stop':
                return self.__execute_stop_command(command, robot)
            case _:
                return InterpretStatus.UNEXPECTED_COMMAND
                
        
# Основная программа

commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop']  

robot = Robot()
interpreter = CommandsInterpreter(robot)

interpreter.interpret(commands)
