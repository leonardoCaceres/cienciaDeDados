import numpy as np
import pandas as pd

from Core.generate import Generate

from Core.Graphic.Implements.graphics import GraphicsImpl
from Core.Report.Implements.reportStates import ReportStates

class StatesAdapter:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    def adapterToReport(self):
        generate = Generate()
        statesBalance = self.dataset['Estados'].to_numpy()
        valuesBalance = self.dataset['Saldo'].to_numpy()
        valuesBudget = self.dataset['Arrecadacao'].to_numpy()
        valuesExpense = self.dataset['Gastos'].to_numpy()


        graphicsBalance = GraphicsImpl(
            statesBalance,
            valuesBalance,
            'Saldo dos Estado',
            'Estados',
            'Total do Saldo'
        )
        generate.generateGraphic(graphicsBalance)

        ######## Gerando relatorios nos txt ########
        reportStates = ReportStates(statesBalance, valuesBudget, valuesExpense, valuesBalance, 2020)
        generate.generateReport(reportStates)
