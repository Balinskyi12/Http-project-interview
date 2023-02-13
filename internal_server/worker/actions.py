import random
import time
import uuid


class IOOperation:
    def __init__(self, order: int = 0):
        self.order = order
        self.id = uuid.uuid4()
        self.name = f"operation {self.id}"
        self.required_progress: int = 50 + random.randint(0, 50)
        self.progress: int = 0
        self.stop = 0
        self.wait = 1
        self.loop = self.process()

    def process(self):
        while not self.ready():
            self.stop = int(time.time()) + self.wait
            self.move()
            yield
            self.report()
            while int(time.time()) < self.stop:
                time.sleep(1)

    def report(self):
        print(f" Progress of {self.name} is {self.progress}")

    def action(self):
        try:
            next(self.loop)
        except StopIteration:
            return True

    def ready(self) -> bool:
        return self.progress >= self.required_progress

    def move(self):
        self.progress += 10
