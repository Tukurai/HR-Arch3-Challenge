import asyncio
import threading
import time
from random import randint


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
        print("Handling this frame's events")
        # The event handling here needs to be adjusted to work properly with asyncio.Queue
        while not self.msg_q.empty():
            item = self.msg_q.get_nowait()
            print(item)
            self.msg_q.task_done()
        time.sleep(1)


class FakeAsyncClient:
    def __init__(self, msg_q):
        self.msg_q: asyncio.Queue = msg_q
        self.running = False

    async def do_operation(self):
        self.running = True
        while self.running:
            await asyncio.sleep(randint(0, 10000) / 20000)
            await self.msg_q.put(randint(0, 1000))
        print("We're done")

    def run(self):
        asyncio.run(self.do_operation())

    def stop(self):
        self.running = False


if __name__ == '__main__':
    test = TestEngine()
    test.run()
    asyncio.sleep(5)
    print("We've reached this far")
    test.msg_client.stop()
