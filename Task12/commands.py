import pure_robot
import command_data

class Command:
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState: ...
    

class MoveCommand(Command):
    def __init__(self, data: command_data.MoveCommandData):
        self.__data = data
        
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(pure_robot.transfer_to_cleaner, self.__data.dist, state)
        
        
class TurnCommand(Command):
    def __init__(self, data: command_data.TurnCommandData):
        self.__data = data
        
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(pure_robot.transfer_to_cleaner, self.__data.angle, state)
        

class SetCommand(Command):
    def __init__(self, data: command_data.SetCommandData):
        self.__data = data
        
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(pure_robot.transfer_to_cleaner, self.__data.mode, state)
     
        
class StartCommand(Command):
    def __init__(self, data: command_data.StartCommandData):
        self.__data = data
        
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(pure_robot.transfer_to_cleaner, state)
        
        
class StopCommand(Command):
    def __init__(self, data: command_data.StartCommandData):
        self.__data = data
        
    def execute(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(pure_robot.transfer_to_cleaner, state)
        
        
class CommandFactory():
    def Create(self, data: command_data.CommandData) -> Command:
        match data.get_command_type():
            case 'move': 
                return MoveCommand(data)
            case 'turn': 
                return TurnCommand(data)
            case 'set': 
                return SetCommand(data)
            case 'start': 
                return StartCommand(data)
            case 'stop': 
                return StopCommand(data)
        