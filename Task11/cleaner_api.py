import pure_robot
from monads import StateMonad
from collections import deque

class RobotApi:

    def setup(self, transfer):
        self.f_transfer = transfer
        self.robot_state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)
    
    
    def move_wrapper(self, dist):
        def wrapper(state):
            new_state = pure_robot.move(self.f_transfer, dist, state)
            return (None, new_state)
        
        return StateMonad(wrapper)
        
        
    def turn_wrapper(self, angle):
        def wrapper(state):
            new_state = pure_robot.turn(self.f_transfer, angle, state)
            return (None, new_state)
        
        return StateMonad(wrapper)
        
        
    def set_wrapper(self, set_state):
        def wrapper(state):
            new_state = pure_robot.set_state(self.f_transfer, set_state, state)
            return (None, new_state)
        
        return StateMonad(wrapper)
        
        
    def start_wrapper(self):
        def wrapper(state):
            new_state = pure_robot.start(self.f_transfer, state)
            return (None, new_state)
        
        return StateMonad(wrapper)
        
        
    def stop_wrapper(self):
        def wrapper(state):
            new_state = pure_robot.stop(self.f_transfer, state)
            return (None, new_state)
        
        return StateMonad(wrapper)    
        
        
    def make(self, code):
        
        handle_chain = StateMonad(lambda state: (None, state))
        
        for command in code:
            cmd = command.split(' ')
            if cmd[0]=='move':
                dist = int(cmd[1])
                handle_chain = handle_chain.bind(lambda _, d=dist: self.move_wrapper(d))
            elif cmd[0]=='turn':
                angle = int(cmd[1])
                handle_chain = handle_chain.bind(lambda _, a=angle: self.turn_wrapper(a))
            elif cmd[0]=='set':
                mode = cmd[1]
                handle_chain = handle_chain.bind(lambda _: self.set_wrapper(mode))
            elif cmd[0]=='start':
                handle_chain = handle_chain.bind(lambda _: self.start_wrapper())
            elif cmd[0]=='stop':
                 handle_chain = handle_chain.bind(lambda _: self.stop_wrapper())
            
            
        (value, result_state) = handle_chain.execute(self.robot_state)    
        
        print(f'\n Result robot state:\n pos({result_state.x}, {result_state.y})\n angle({result_state.angle})\n state({result_state.state})')
            
        return result_state
    

    def __call__(self, code):
        return self.make(code)


def transfer_to_cleaner(message):
    print (message)

api = RobotApi()    

api.setup(transfer_to_cleaner)