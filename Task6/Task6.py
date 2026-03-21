import math
from collections import namedtuple

Position = namedtuple("Position", "x y")
CleanMode = namedtuple("CleanMode", "mode")

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка щётками


# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message):
    print (message)

# Функции опрашивют о состоянии непосредственно самого робота, система не хранит его состояние.
def get_cleaner_coordinate() -> Position:
    return Position(0.0, 0.0)
    
def get_cleaner_angle() -> float:
    return 0.0
    
def get_cleaner_states() -> int:
    return WATER


# перемещение
def move(transfer, position_source, angle_source, dist):
    angle_rads = angle_source() * (math.pi/180.0)   
    position = position_source()
    new_position = Position(
        position.x + dist * math.cos(angle_rads),
        position.y + dist * math.sin(angle_rads))  
    transfer(('POS(',new_state.x,',',new_state.y,')'))

# поворот
def turn(transfer, angle_source, turn_angle):
    angle = angle_source()
    new_angle = angle + turn_angle
    transfer(('ANGLE', new_angle))

# установка режима работы
def set_state(transfer, cleaner_state_source, new_internal_state):
    if new_internal_state=='water':
        self_state = WATER  
    elif new_internal_state=='soap':
        self_state = SOAP
    elif new_internal_state=='brush':
        self_state = BRUSH
    else:
        self_state = cleaner_state_source()  

    transfer(('STATE',self_state))

# начало чистки
def start(transfer, cleaner_state_source):
    transfer(('START WITH', cleaner_state_source()))

# конец чистки
def stop(transfer):
    transfer(('STOP',))


# интерпретация набора команд
def make(transfer, cleaner_coordinate_source, cleaner_angle_source, cleaner_states_source, code):
    for command in code:
        cmd = command.split(' ')
        if cmd[0]=='move':
             move(transfer, cleaner_coordinate_source, cleaner_angle_source, int(cmd[1])) 
        elif cmd[0]=='turn':
             turn(transfer, cleaner_angle_source, int(cmd[1]))
        elif cmd[0]=='set':
             set_state(transfer, cleaner_states_source, cmd[1]) 
        elif cmd[0]=='start':
             start(transfer, cleaner_states_source)
        elif cmd[0]=='stop':
             stop(transfer)
    
