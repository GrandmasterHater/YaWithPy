from pure_robot import RobotState

def get_x(get_state) -> RobotState:
        return get_state().x

def get_y(get_state) -> RobotState:
    return get_state().y

def get_angle(get_state) -> RobotState:
    return get_state().angle

def get_state(get_state) -> RobotState:
    return get_state().state


def activate_cleaner(make, code, state) -> RobotState:
    return make(transfer_to_cleaner, code, state)
    
# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message):
    print (message)