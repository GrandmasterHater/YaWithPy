import pure_robot 
import cleaner_api

state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

# главная программа
get_state = lambda: state

state = cleaner_api.activate_cleaner(pure_robot.make, ('move 100', 'turn -90', 'set soap', 'start', 'move 50', 'stop'), state)

print (cleaner_api.get_x(get_state), 
    cleaner_api.get_y(get_state), 
    cleaner_api.get_angle(get_state), 
    cleaner_api.get_state(get_state))