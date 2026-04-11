from collections import namedtuple
from enum import StrEnum
import math
from events import *
from event_repository import EventStorage


RobotState = namedtuple("RobotState", "x y angle mode")


class Mode(StrEnum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"



class MoveProcessor:
    def __init__(self, store: EventStorage):
        self.__store = store
        self.__queue = store.register_listener(REQUESTS)
       
        
    def __get_next_state(self, current_state: tuple[float, float, float], event: Event) -> tuple[float, float, float]:
        x, y, angle = current_state
        
        match event:
            case MovedEvent(x=ex, y=ey): x, y = ex, ey
            case TurnedEvent(angle=a):   angle = a
            
        return x, y, angle


    def __restore(self) -> tuple[float, float, float]:
        x, y, angle = 0.0, 0.0, 0.0
        
        for event in self.__store.load(RESULTS):
            x, y, angle = self.__get_next_state((x, y, angle), event)
            
        return x, y, angle


    async def run(self):
        while True:
            event = await self.__queue.get()
            
            if not isinstance(event, MoveRequestedEvent):
                continue
            
            x, y, angle = self.__restore()
            
            rads = angle * (math.pi / 180.0)
            x += event.dist * math.cos(rads)
            y += event.dist * math.sin(rads)
            
            await self.__store.publish(
                MovedEvent(version=0, x=x, y=y), 
                RESULTS
            )



class TurnProcessor:
    def __init__(self, store: EventStorage):
        self.__store = store
        self.__queue = store.register_listener(REQUESTS)
        
        
    def __get_next_angle(self, current_angle: float, event: Event) -> tuple[float, float, float]:
        angle = current_angle
        
        match event:
                case TurnedEvent(angle=a):   angle = a
                
        return angle  


    def __restore(self) -> float:
        angle = 0.0
        
        for event in self.__store.load(RESULTS):
            angle = self.__get_next_angle(angle, event)
            
        return angle


    async def run(self):
        while True:
            event = await self.__queue.get()
            if not isinstance(event, TurnRequestedEvent):
                continue
            await self.__store.publish(
                TurnedEvent(version=0, angle=self.__restore() + event.angle),
                RESULTS,
            )



class ModeProcessor:
    def __init__(self, store: EventStorage):
        self.__store = store
        self.__queue = store.register_listener(REQUESTS)


    async def run(self):
        while True:
            event = await self.__queue.get()
            if not isinstance(event, SetModeRequestedEvent):
                continue
            await self.__store.publish(
                SetModeEvent(version=0, mode=event.mode), 
                RESULTS
            )



class StartStopProcessor:
    def __init__(self, store: EventStorage):
        self.__store = store
        self.__queue = store.register_listener(REQUESTS)


    async def run(self):
        while True:
            event = await self.__queue.get()
            
            match event:
                case StartRequestedEvent():
                    result = StartedEvent(version=0)
                case StopRequestedEvent():
                    result = StopedEvent(version=0)
                case _:
                    continue
                
            await self.__store.publish(result, RESULTS)



class RobotStateAggregator:
    def __init__(self, store: EventStorage):
        self.__store = store
        self.__queue = store.register_listener(RESULTS)
        self.__x       = 0.0
        self.__y       = 0.0
        self.__angle   = 0.0
        self.__mode    = 0
        self.__running = False


    def __apply(self, event: Event):
        match event:
            case MovedEvent(x=x, y=y): self.__x, self.__y = x, y
            case TurnedEvent(angle=a): self.__angle = a
            case SetModeEvent(mode=m): self.__mode = m
            case StartedEvent():       self.__running = True
            case StopedEvent():        self.__running = False


    def __print(self):
        print( "Current state:\n"
            f"pos x={self.__x} y={self.__y}\n"
            f"angle={self.__angle:}\n"
            f"mode={self.__mode}\n"
            f"running={self.__running}\n"
        )

    async def run(self):
        while True:
            event = await self.__queue.get()
            self.__apply(event)
            self.__print()
            
            
            