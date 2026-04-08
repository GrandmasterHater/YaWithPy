from robot_events import RobotEvent

class EventRepository:
    def __init__(self):
        self.__snapshot: RobotEvent
        self.__srotage: RobotEvent = list()
        
    def fetch(self) -> list[RobotEvent]:
        return self.__srotage
        
    def append(self, event: RobotEvent):
        self.__srotage.append(event)