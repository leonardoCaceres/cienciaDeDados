from abc import ABC, abstractmethod
from typing import List

class ReportInterface:

    @abstractmethod
    def createReport(self) -> None:
        pass

    @abstractmethod
    def calculateBalance(self, budget: List[str], expense: List[str]) -> List[float]:
        pass
    
    @abstractmethod
    def determinar_quartil(self, valor: float, q1: float, q2: float, q3: float) -> str:
        pass
    
