import asyncio
import threading
import time
from random import randint

from Settings import settings


class TestEngine:
    def __init__(self):
        self.msg_q = asyncio.Queue()
        self.msg_client = FakeAsyncClient(self.msg_q)
        # Start a new thread that runs the event loop
        threading.Thread(target=self.msg_client.run, daemon=True).start()

    def run(self):
        while True:
            self.handle_events()

    def handle_events(self):
        if(settings.DEBUG_MODE): print("Handling this frame's events")
        # The event handling here needs to be adjusted to work properly with asyncio.Queue
        while not self.msg_q.empty():
            item = self.msg_q.get_nowait()
            if(settings.DEBUG_MODE): print(item)
            self.msg_q.task_done()
        time.sleep(1)


class FakeAsyncClient:
    def __init__(self, msg_q):
        self.msg_q: asyncio.Queue = msg_q

    async def do_operation(self):
        while True:
            await asyncio.sleep(randint(0, 10000) / 20000)
            await self.msg_q.put(randint(0, 1000))

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.do_operation())
        loop.close()


if __name__ == '__main__':
    test = TestEngine()
    test.run()