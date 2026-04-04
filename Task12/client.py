from command_data import MoveCommandData, TurnCommandData, SetCommandData, StartCommandData, StopCommandData
from cleaner_api import api
    
commands = (
    MoveCommandData(100),
    TurnCommandData(-90),
    SetCommandData('soap'),
    StartCommandData(),
    MoveCommandData(50),
    StopCommandData()
    )


api(commands)