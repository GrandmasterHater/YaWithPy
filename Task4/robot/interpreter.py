from typing import List
from .interpret_status import InterpretStatus
from .robot import Robot
from .setmode import SetMode

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