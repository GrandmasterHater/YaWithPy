from event_repository import EventStorage
from events import Event, MoveRequestedEvent, TurnRequestedEvent, SetModeRequestedEvent, StartRequestedEvent, StopRequestedEvent, REQUESTS, RESULTS

class CommandHandler:
    def __init__(self, store: EventStorage):
        self._store = store

    async def handle(self, command: str):
        cmd = command.split()
        match cmd[0]:
            case 'move':
                event = MoveRequestedEvent(version=0, dist=int(cmd[1]))
            case 'turn':
                event = TurnRequestedEvent(version=0, angle=int(cmd[1]))
            case 'set':
                event = SetModeRequestedEvent(version=0, mode=cmd[1])
            case 'start':
                event = StartRequestedEvent(version=0)
            case 'stop':
                event = StopRequestedEvent(version=0)

        await self._store.publish(event, REQUESTS)
