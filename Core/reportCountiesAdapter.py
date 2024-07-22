import numpy as np
import pandas as pd

from Core.generate import Generate

from Core.Report.Implements.reportCounties import ReportCounties

class ReportCountiesAdapter:
    def __init__(self, dataset: pd.DataFrame, year: int):
        self.dataset = dataset
        self.year = year

    def adapterToReport(self):
        generate = Generate()
        
        reportCounties = ReportCounties(
            self.dataset["Municipios"].to_numpy(),
            self.dataset["Arrecadacao"].to_numpy(),
            self.dataset["Gastos"].to_numpy(),
            self.dataset["Populacao"].to_numpy(),
            self.year
        )

        generate.generateReport(reportCounties)
