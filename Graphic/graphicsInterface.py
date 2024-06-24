from abc import ABC, abstractmethod

class GraphicsInterface:
    
    @abstractmethod
    def createGraphics(self) -> None:
        pass
