import matplotlib.pyplot as plt
from typing import List

class Graphics:
    def createGraphics(
            self,
            names: List[str],
            values: List[float],
            title: str,
            name: str,
            description: str
        ) -> None:
        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.bar(names, values, color='skyblue', edgecolor='black')

        # Adicionando título e rótulos
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(name, fontsize=14)
        ax.set_ylabel(description, fontsize=14)

        plt.bar(names, values)
        plt.show()
