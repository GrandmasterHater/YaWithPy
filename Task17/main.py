from commands import *
from angle import AngleDeg360
from coordinate import Coordinate
from robot import CleaningMode, RobotCleaner

robot = RobotCleaner(Coordinate(0.0, 0.0), AngleDeg360(0.0), CleaningMode.WATER)

commands = [MoveCommand(100),
            TurnCommand(AngleDeg360(-90)),
            SetStateCommand(CleaningMode.SOAP),
            StartCommand(),
            MoveCommand(50),
            StopCommand()]
            
command_executor = CommandExecutor()

command_results, robot = command_executor.execute_all(commands, robot)

for result in command_results:
    print(f'{result}\n\n\n')
    
print(f'Current state:\n{robot}')