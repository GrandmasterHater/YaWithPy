class CommandData:
    def get_command_type(self) -> str: ...
        
        
class MoveCommandData(CommandData):
    def __init__(self, dist: int):
        self.dist = dist
        
    def get_command_type(self):
        return 'move'
        
        
class TurnCommandData(CommandData):
    def __init__(self, angle: int):
        self.angle = angle
        
    def get_command_type(self):
        return 'turn'
        
        
class SetCommandData(CommandData):
    def __init__(self, mode: str):
        self.mode = mode
        
    def get_command_type(self):
        return 'set'
        
        
class StartCommandData(CommandData):
        
    def get_command_type(self):
        return 'start'
        
        
class StopCommandData(CommandData):
        
    def get_command_type(self):
        return 'stop'
        