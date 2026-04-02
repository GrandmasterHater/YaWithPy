class Monad:
    def __init__(self, state):
        self.state = state
        
    def bind(self, func):
        return func(self.state)
        

class StateMonad:
    def __init__(self, func):
        self.__func = func
        
    def execute(self, state):
        return self.__func(state)
        
    def bind(self, continuation_func):
        def func_wrapper(state):
            (current_value, result_state) = self.__func(state)
            new_state_monad = continuation_func(current_value)
            return new_state_monad.execute(result_state)
        
        return StateMonad(func_wrapper)
        
