from collections import namedtuple
import math
from typing import List, Callable, Dict

class MoveResponse:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"

class SetStateResponse:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"

RobotState = namedtuple("RobotState", "x y angle state")


WATER = 1  
SOAP = 2   
BRUSH = 3  


def get_available_move_actions(state: RobotState, log: List[str]) -> Dict[Callable, Callable]:
    available_actions: Dict[Callable, Callable] = { move:lambda dist:  move(dist, state, log),
                                                    turn:lambda angle: turn(angle, state, log)}
    angle_rads = state.angle * (math.pi / 180.0)
    dir_x = round(math.cos(angle_rads), 3)
    dir_y = round(math.sin(angle_rads), 3)

    is_faicing_outside_on_x: bool = (state.x <= 0 and dir_x < 0) or (state.x >= 100 and dir_x > 0)
    is_faicing_outside_on_y: bool = (state.y <= 0 and dir_y < 0) or (state.y >= 100 and dir_y > 0)

    if is_faicing_outside_on_x or is_faicing_outside_on_y:
        available_actions.pop(move)

    return available_actions
   
    
def get_available_set_actions(state: RobotState, log: List[str]) -> Dict[Callable, Callable]:
    available_actions: Dict[Callable, Callable] = {set_state: lambda mode:  set_state(mode, state, log)}

    if check_resources(WATER) != SetStateResponse.OK or check_resources(SOAP) != SetStateResponse.OK:
        available_actions.pop(set_state)

    return available_actions
    
    
def get_available_actions(new_state, log):
    return get_available_move_actions(new_state, log) | get_available_set_actions(new_state, log)


def check_position(x: float, y: float) -> tuple[float, float, str]:
    constrained_x = max(0, min(100, x))
    constrained_y = max(0, min(100, y))
    
    if x == constrained_x and y == constrained_y:
        return (x, y, MoveResponse.OK)
    return (constrained_x, constrained_y, MoveResponse.BARRIER)


def check_resources(new_mode: int) -> SetStateResponse:
    if new_mode == WATER:
        # ....
        return SetStateResponse.NO_WATER
    elif new_mode == SOAP:
        # ....
        return SetStateResponse.NO_SOAP
    return SetStateResponse.OK


def move(dist, old_state, log):
    angle_rads = old_state.angle * (math.pi/180.0)
    new_x = old_state.x + dist * math.cos(angle_rads)
    new_y = old_state.y + dist * math.sin(angle_rads)
    
    constrained_x, constrained_y, move_result = check_position(new_x, new_y)
    
    new_state = RobotState(
        constrained_x,
        constrained_y,
        old_state.angle,
        old_state.state
    )
    
    message = (f'POS({int(constrained_x)},{int(constrained_y)})' 
              if move_result == MoveResponse.OK 
              else f'HIT_BARRIER at ({int(constrained_x)},{int(constrained_y)})')
              
    new_log = log + [message]
    
    available_actions: Dict[Callable, Callable] = get_available_actions(new_state, new_log)
    
    return available_actions, new_state, new_log


def turn(angle, old_state, log):
    new_state = RobotState(
        old_state.x,
        old_state.y,
        old_state.angle + angle,
        old_state.state
    )
    new_log = log + [f'ANGLE {new_state.angle}']
    available_actions: Dict[Callable, Callable] = get_available_actions(new_state, new_log)
    
    return available_actions, new_state, new_log


def set_state(new_mode, old_state, log):
    resource_check = check_resources(new_mode)
    
    if resource_check != SetStateResponse.OK:
        message = f'RESOURCE ERROR: {resource_check} for mode {new_mode}'
        return old_state, log + [message], resource_check
    
    new_state = RobotState(
        old_state.x,
        old_state.y,
        old_state.angle,
        new_mode
    )
    
    new_log = log + [f'STATE {new_mode}']
    available_actions: Dict[Callable, Callable] = get_available_actions(new_state, new_log)
    
    return available_actions, new_state, new_log
 
   
    
state = RobotState(0.0, 0.0, 0, WATER)
log = []
available_actions: Dict[Callable, Callable] = get_available_actions(state, log)
             
if available_actions.get(move) is not None:
    available_actions, state, log = available_actions[move](150)
    
if available_actions.get(set_state) is not None:
    available_actions, state, log = available_actions[set_state](SOAP)
    
if available_actions.get(turn) is not None:
    available_actions, state, log = available_actions[turn](90)
    
if available_actions.get(move) is not None:
    available_actions, state, log = available_actions[move](50)
    
    
print(f"Final state: {state}")
print(f"Log: {log}")
