import dataclasses
from collections import defaultdict
from queue import Queue
from events import Event
import asyncio

class EventStorage:
    def __init__(self):
        self._store: defaultdict[str, list[Event]] = defaultdict(list)
        self._listeners: defaultdict[str, list[asyncio.Queue]] = defaultdict(list)

    def register_listener(self, stream_id: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._listeners[stream_id].append(queue)
        return queue

    def unregister_listener(self, stream_id: str, channel: asyncio.Queue):
        self._listeners[stream_id].remove(channel)

    async def publish(self, event: Event, stream_id: str) -> Event:
        version = len(self._store[stream_id]) + 1
        event = dataclasses.replace(event, version=version)
        self._store[stream_id].append(event)
        for queue in self._listeners[stream_id]:
            await queue.put(event)
        return event

    def load(self, stream_id: str) -> list[Event]:
        return list(self._store[stream_id])