from typing import Protocol
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1 # полив водой
SOAP  = 2 # полив мыльной пеной
BRUSH = 3 # чистка щётками

class RobotProtocol(Protocol):
    def transfer_to_cleaner(message): ...

    # перемещение
    def move(dist, state): ...

    # поворот
    def turn(turn_angle, state): ...

    # установка режима работы
    def set_state(new_internal_state, state): ...

    # начало чистки
    def start(state): ...

    # конец чистки
    def stop(state): ...

    # интерпретация набора команд
    def make(code, state): ...