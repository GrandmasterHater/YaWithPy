import pure_robot

class RobotCommandsApi:
    def __init__(self):
        self.__robot_state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)
        
    def send_commands(self, commands):
        self.__robot_state = pure_robot.make(pure_robot.transfer_to_cleaner, commands, self.__robot_state);
            
            

commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'] 

commands_api = RobotCommandsApi()

commands_api.send_commands(commands)