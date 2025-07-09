from abc import ABC, abstractmethod
from typing import Dict, Any
from graphdatascience import GraphDataScience


class AlgorithmHandler(ABC):
    def __init__(self, gds: GraphDataScience):
        self.gds = gds

    @abstractmethod
    def execute(self, arguments: Dict[str, Any]) -> Any:
        pass
