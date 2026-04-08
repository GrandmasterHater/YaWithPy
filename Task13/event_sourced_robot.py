from collections import namedtuple
from enum import StrEnum
import math
from robot_events import RobotEvent, MoveEvent, TurnEvent, SetModeEvent, StartEvent, StopEvent

RobotState = namedtuple("RobotState", "x y angle mode")


class Mode(StrEnum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


class EventSourcedRobot:
    def __init__(self, events: list[RobotEvent]):
        self.__robot_state: RobotState = RobotState(0, 0, 0, Mode.WATER)
        self.__version = 0
        self.__load_state(events)
        
        
    def move(self, dist: int) -> RobotEvent:
        angle_rads = self.__robot_state.angle * (math.pi/180.0)  
        new_x = self.__robot_state.x + dist * math.cos(angle_rads)
        new_y = self.__robot_state.y + dist * math.sin(angle_rads)
        new_version = self.__version + 1
        
        return MoveEvent(new_version, new_x, new_y)  
    
    
    def turn(self, turn_angle: float) -> RobotEvent:
        new_angle = self.__robot_state.angle + turn_angle
        new_version = self.__version + 1
        
        return TurnEvent(new_version, new_angle)
    
        
    def set_mode(self, mode: str) -> RobotEvent:
        new_mode = Mode(mode)
        new_version = self.__version + 1
        
        return SetModeEvent(new_version, new_mode)
      
        
    def start(self) -> RobotEvent:
        new_version = self.__version + 1
        
        return StartEvent(new_version)
        
    
    def stop(self) -> RobotEvent:
        new_version = self.__version + 1
        
        return StopEvent(new_version)
        
        
    def __load_state(self, events: list[RobotEvent]):
        for event in events:
            self.__apply_event(event)
            
    def __apply_event(self, event: RobotEvent):
        match event:
            case MoveEvent(version=ver, x=x, y=y):
                self.__robot_state = RobotState(x, y, self.__robot_state.angle, self.__robot_state.mode)
                self.__version = ver
            case TurnEvent(version=ver, angle=angle):
                self.__robot_state = RobotState(self.__robot_state.x, self.__robot_state.y, angle, self.__robot_state.mode)
                self.__version = ver
            case SetModeEvent(version=ver, mode=mode):
                self.__robot_state = RobotState(self.__robot_state.x, self.__robot_state.y, self.__robot_state.angle, mode)
                self.__version = ver
            case StartEvent(version=ver):
                self.__version = ver
            case StopEvent(version=ver):
                self.__version = ver
        