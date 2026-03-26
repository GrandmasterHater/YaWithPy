import pure_robot 
import cleaner_api

state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

def save_state(new_state: pure_robot.RobotState):
    global state
    state = new_state

# главная программа
get_state = lambda: state

commands_handler = cleaner_api.get_commands_handler(get_state, save_state, pure_robot.transfer_to_cleaner, pure_robot.move, pure_robot.turn, pure_robot.start, pure_robot.stop, pure_robot.set_state)

commands_handler((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
    ))

print (cleaner_api.get_x(get_state), 
    cleaner_api.get_y(get_state), 
    cleaner_api.get_angle(get_state), 
    cleaner_api.get_state(get_state))