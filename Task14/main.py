from command_handler import CommandHandler
from event_repository import EventStorage
from robot_processors import MoveProcessor, TurnProcessor, ModeProcessor, StartStopProcessor, RobotStateAggregator
import asyncio


async def main():
    store = EventStorage()
    handler = CommandHandler(store)

    processors = [
        MoveProcessor(store),
        TurnProcessor(store),
        ModeProcessor(store),
        StartStopProcessor(store),
        RobotStateAggregator(store),
    ]

    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'] 

    tasks = [asyncio.create_task(p.run()) for p in processors]
    await asyncio.sleep(0)
    
    # Слипы дают время на обработку 
    
    for command in commands:
        await handler.handle(command)
        await asyncio.sleep(0)
        
    await asyncio.sleep(0)

    for task in tasks:
        task.cancel()


asyncio.run(main())