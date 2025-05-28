from abc import ABC, abstractmethod
from typing import Dict, Any


class AlgorithmHandler(ABC):
    def __init__(self, db_url: str, username: str, password: str):
        self.db_url = db_url
        self.username = username
        self.password = password

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Any:
        pass