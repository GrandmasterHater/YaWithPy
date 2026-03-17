import math

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка метлой
COMMAND_INDEX = 0
COMMAND_ARG_INDEX = 1

def move(dist: int, angle: int, x: float, y:float) -> tuple[float, float]:
    angle_rads = angle * (math.pi/180.0)
    x += dist * math.cos(angle_rads)
    y += dist * math.sin(angle_rads)
    return (x, y)
    
def turn(angle: str, current_angle: int) -> int:
    current_angle += int(angle)
    return current_angle

def set(mode: str) -> int:
    if mode =='water':
        return WATER  
    elif mode =='soap':
        return SOAP
    elif mode =='brush':
        return BRUSH
    else:
        return -1
        

# входная программа управления роботом
code = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

# текущий режим работы устройства очистки
state = WATER

# текущие позиция и угол (ориентация) робота
x = 0.0
y = 0.0
angle = 0

# главная программа
for commandRaw in code:
    command = commandRaw.split(' ')
        
    match command[COMMAND_INDEX].lower():
        case 'move':
            (x, y) = move(int(command[COMMAND_ARG_INDEX]), angle, x, y)
            print(f'POS ({x}, {y})')
        case 'turn':
            angle = turn(command[COMMAND_ARG_INDEX], angle)
            print(f'ANGLE {angle}')
        case 'set':
            state = set(command[COMMAND_ARG_INDEX])
            print(f'STATE {state}')
        case 'start':
            print(f'START WITH {state}')
        case 'stop':
            print('STOP')
        case _:
            print('Unexpected command!')
