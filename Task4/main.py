from robot import Robot, CommandsInterpreter


# взаимодействие с роботом вынесено в отдельную функцию
def transfer_to_cleaner(message):
    print (message)

# Основная программа

commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop']  

robot = Robot(transfer_to_cleaner)
interpreter = CommandsInterpreter(robot)

interpreter.interpret(commands)