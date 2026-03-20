from enum import Enum

class InterpretStatus(Enum):
    OK = 0
    UNEXPECTED_COMMAND = 1
    INVALID_COMMAND_ARGUMENT = 2
    MISSING_COMMAND_ARGUMENT = 3