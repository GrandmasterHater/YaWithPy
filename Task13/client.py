import cleaner_api
    
commands = [
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop']  


cleaner_api.handle_commands(commands)