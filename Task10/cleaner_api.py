import pure_robot
from collections import deque

class RobotApi:

    def setup(self, fn, transfer):
        self.f_transfer = transfer
        self.fn = fn
        
        
    def read_command_stream(self, stream: str):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
        
        datas = stream.split(' ')
        stack = deque()
        
        
        for data in datas:
            fun = self.fn(data)
            stack.append(data)
            
            if fun != None:
                self.execute_command(fun, stack)
                stack = deque()
      
                

    def execute_command(self, fun, command_stack):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
                 
        command = command_stack.pop();
        
        if command=='move':
             arg = command_stack.pop()
             self.cleaner_state = fun(self.f_transfer, int(arg), self.cleaner_state) 
        elif command=='turn':
            arg = command_stack.pop()
            self.cleaner_state = fun(self.f_transfer, int(arg), self.cleaner_state)
        elif command=='set':
            arg = command_stack.pop()
            self.cleaner_state = fun(self.f_transfer, arg, self.cleaner_state) 
        elif command=='start':
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
        elif command=='stop':
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
        return self.cleaner_state
    

    def __call__(self, stream):
        return self.read_command_stream(stream)


def transfer_to_cleaner(message):
    print (message)

def robotFn(cmd):
    if cmd=='move':
        return pure_robot.move
    elif cmd=='turn':
        return pure_robot.turn  
    elif cmd=='set':
        return pure_robot.set_state 
    elif cmd=='start':
        return pure_robot.start
    elif cmd=='stop':
        return pure_robot.stop 
    return None

api = RobotApi()    

api.setup(robotFn, transfer_to_cleaner)