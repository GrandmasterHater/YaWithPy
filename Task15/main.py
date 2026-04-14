from functools import wraps
from collections import namedtuple
import math

RobotState = namedtuple("RobotState", "x y angle state water_count soap_count")


class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"
    

class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"
    

WATER = 1  
SOAP = 2   
BRUSH = 3  

class StateMonad:
    def __init__(self, state, log=None):
        self.state = state
        self.log = log or []
    
    def bind(self, func):
        new_state, new_log = func(self.state, self.log)
        return StateMonad(new_state, new_log)

def move(dist):
    def inner(old_state, log):
        angle_rads = old_state.angle * (math.pi/180.0)
        new_state = RobotState(
            old_state.x + dist * math.cos(angle_rads),
            old_state.y + dist * math.sin(angle_rads),
            old_state.angle,
            old_state.state,
            old_state.water_count,
            old_state.soap_count
        )
        return new_state, log + [f'POS({int(new_state.x)},{int(new_state.y)})']
    return inner

def turn(angle):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle + angle,
            old_state.state,
            old_state.water_count,
            old_state.soap_count
        )
        return new_state, log + [f'ANGLE {new_state.angle}']
    return inner

def set_state(new_mode):
    def inner(old_state, log):
        new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_mode,
            old_state.water_count,
            old_state.soap_count
        )
        return new_state, log + [f'STATE {new_mode}']
    return inner

def start(old_state, log):
    return old_state, log + ['START']

def stop(old_state, log):
    return old_state, log + ['STOP']
    
    
def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))
    
    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)


def check_resources(new_mode: int, water_count: float, soap_count: float) -> SetStateResponse:
    if new_mode == WATER and water_count < 0.05:
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP and soap_count < 0.05:
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK
    
    
def validate_move(old_state, log):
    x, y, status = check_position(old_state.x, old_state.y)
        
    if status == MoveResponse.BARRIER:
        new_state = RobotState(
            x,
            y,
            old_state.angle,
            old_state.state,
            old_state.water_count,
            old_state.soap_count)
    else:
        new_state = old_state
            
    log_message = f"Pos. valid ({int(new_state.x)},{int(new_state.y)})" if status == MoveResponse.OK else f"Pos. constrained x({int(old_state.x)} -> {int(new_state.x)}) y({int(old_state.y)} -> {int(new_state.y)})"
    return new_state, log + [log_message]
    

def validate_resources(old_state, log):
    status = check_resources(old_state.state, old_state.water_count, old_state.soap_count)
    
    if status == SetStateResponse.NO_WATER or status == SetStateResponse.NO_SOAP:
        new_set_state = BRUSH
    else:
        new_set_state = old_state.state
        
    new_state = RobotState(
            old_state.x,
            old_state.y,
            old_state.angle,
            new_set_state,
            old_state.water_count,
            old_state.soap_count) 
            
    log_message = SetStateResponse.OK if status == SetStateResponse.OK else f'Res. status: {status}. Fallback to brush.'
    return new_state, log + [log_message]


states = [RobotState(0.0, 0.0, 0, WATER, 1.0, 1.0),
          RobotState(0.0, 0.0, 0, WATER, 0.03, 1.0),
          RobotState(0.0, 0.0, 0, WATER, 1.0, 0.03)]
          
dist = [100, 150, 100]
modes = [BRUSH, WATER, SOAP]
          
for index in range(3):
    initial_state = StateMonad(states[index])
    result = (initial_state
        .bind(move(dist[index]))
        .bind(validate_move)
        .bind(turn(-90))
        .bind(set_state(modes[index]))
        .bind(validate_resources)
        .bind(start)
        .bind(move(50))
        .bind(stop))

    print(f"Final state: {result.state}")
    print(f"Log: {result.log} \n\n\n")
