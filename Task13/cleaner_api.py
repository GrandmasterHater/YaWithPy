from event_repository import EventRepository
from event_sourced_robot import EventSourcedRobot
from robot_events import RobotEvent

__repository = EventRepository()

def handle_commands(commands):
    
    for command in commands:
        
        events = __repository.fetch()
        robot = EventSourcedRobot(events)
        
        cmd = command.split(' ')
        new_event: RobotEvent
        
        match cmd[0]:
            case 'move':
                new_event = robot.move(int(cmd[1]))
            case 'turn':
                new_event = robot.turn(int(cmd[1]))
            case 'set':
                new_event = robot.set_mode(cmd[1])
            case 'start':
                new_event = robot.start()
            case 'stop':
                new_event = robot.stop()
                
        __repository.append(new_event)
        
    
    events = __repository.fetch()
    
    print('Events:')
    
    for event in events:
        print(event)
                

