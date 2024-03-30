import json
from typing import Dict, Any
import os
from datetime import datetime

class BaseStorage:
    def save_state(self, state: Dict[str, Any]) -> None:
        pass

    def retrieve_state(self) -> Dict[str, Any]:
        pass

class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def save_state(self, state: Dict[str, Any]) -> None:
        with open(self.file_path, 'w') as file:
            json.dump(state, file)

    def retrieve_state(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r') as file:
            return json.load(file)

class State:
    def __init__(self, storage: JsonFileStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%dT%H:%M:%S.%f')

        state = self.storage.retrieve_state()
        state[key] = value
        self.storage.save_state(state)

    def get_state(self, key: str, default=None) -> Any:
        state = self.storage.retrieve_state()
        return state.get(key, default)
