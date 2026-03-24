from cleaner_api import CleanerApi
from robot_protocol_adapter import RobotAdapter

# главная программа

robot_adapter = RobotAdapter()
cleaner_api = CleanerApi(robot_adapter)

cleaner_api.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ))

print (cleaner_api.get_x(), 
    cleaner_api.get_y(), 
    cleaner_api.get_angle(), 
    cleaner_api.get_state())