import pure_robot
import commands

class RobotApi:
    def __init__(self):
        self.__command_factory = commands.CommandFactory()
        self.__state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)
        
        
    def make(self, command_datas):
        commands = []
        
        for data in command_datas:
            command = self.__command_factory.Create(data)
            commands.append(command)
            
        self.__state = self.fold(commands, self.__state)
            
        return self.__state
        
        
    def fold(self, commands: list[commands.Command], start_state: pure_robot.RobotState) -> pure_robot.RobotState:
        current_state = start_state
        
        for command in commands:
            current_state = command.execute(current_state)
            
        return current_state

    def __call__(self, commands):
        return self.make(commands)


api = RobotApi()    