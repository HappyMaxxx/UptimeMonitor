# Temporary db
from typing import Dict

from app.schemas.targets import Target


class IdCounter():
    def __init__(self, start: int = 1):
        self._id: int = start

    def get_next(self) -> int:
        # Returns IdCouner._id and increase it
        temp = self._id
        self._id += 1
        return temp

    def clear(self) -> None:
        # Reset counter
        self._id = 1
        return None

class InMemoryDB:
    def __init__(self):
        self.targets: Dict[int, Target] = {}
        self.counter = IdCounter()
    
    def add_target(self, target: Target) -> Target:
        target.id = self.counter.get_next()
        self.targets[target.id] = target
        return target
    
    def get_target(self, target_id: int) -> Target:
        return self.targets.get(target_id)


db = InMemoryDB()