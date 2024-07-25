import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from typing import List

from Core.Graphic.graphicsInterface import GraphicsInterface

class GraphicsImpl(GraphicsInterface):

    def __init__(
            self,
            names: List[str],
            values: List[float],
            title: str,
            name: str,
            description: str
        ):
        self.names = names
        self.values = values
        self.title = title
        self.name = name
        self.description = description + " em milhares de reais"
    
    def createGraphics(self) -> None:
        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.bar(self.names, self.values, color='skyblue', edgecolor='black')

        # Adicionando título e rótulos
        ax.set_title(self.title, fontsize=16)
        ax.set_xlabel(self.name, fontsize=14)
        ax.set_ylabel(self.description, fontsize=14)

        # Definindo a escala logarítmica para o eixo y
        ax.set_yscale('log')

        # Formatando os rótulos do eixo y para mostrar valores em bilhões
        formatter = FuncFormatter(lambda y, _: f'{y / 1e9:.1f}B')
        ax.yaxis.set_major_formatter(formatter)

        plt.bar(self.names, self.values)
        plt.show()
