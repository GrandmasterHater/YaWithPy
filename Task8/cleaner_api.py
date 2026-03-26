from pure_robot import RobotState

def get_x(get_state: RobotState):
        return get_state().x

def get_y(get_state: RobotState):
    return get_state().y

def get_angle(get_state: RobotState):
    return get_state().angle

def get_state(get_state: RobotState):
    return get_state().state


def get_commands_handler(get_state, save_state, transfer, move, turn, start, stop, set_state):
    def activate_cleaner(code):
        for command in code:
        
            cleaner_state = get_state()
            cmd = command.split(' ')
                
            if cmd[0]=='move':
                cleaner_state = move(transfer, int(cmd[1]), cleaner_state) 
            elif cmd[0]=='turn':
                cleaner_state = turn(transfer, int(cmd[1]), cleaner_state)
            elif cmd[0]=='set':
                cleaner_state = set_state(transfer, cmd[1], cleaner_state) 
            elif cmd[0]=='start':
                cleaner_state = start(transfer, cleaner_state)
            elif cmd[0]=='stop':
                cleaner_state = stop(transfer, cleaner_state)
                    
            save_state(cleaner_state)
                
    return activate_cleaner