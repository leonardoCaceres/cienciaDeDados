import numpy as np
import pandas as pd

from Core.generate import Generate

from Core.Graphic.Implements.graphics import GraphicsImpl

from Core.Report.Implements.reportCounties import ReportCounties
from Core.Report.Implements.reportStates import ReportStates

class DataReaderTemplate:
    
    def __init__(self, pathExpense: str, pathBudget: str, year: int):
        self.pathExpense = pathExpense
        self.pathBudget = pathBudget
        self.year = year
    
    def openfile(self, path: str) -> pd.DataFrame:
        data = pd.read_csv(
        path, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
        )
        return data
    
    def cleanData(self, dataFrame: pd.DataFrame, population: bool) -> pd.DataFrame:
        dataFrame.drop(columns=['Identificador da Conta'], inplace=True)
        dataFrame.drop(columns=['Cod.IBGE'], inplace=True)
        if population:
            dataFrame.drop(columns=['População'], inplace=True)
        
        return dataFrame
    
    def initialization(self) -> None:
        generate = Generate()

        ######## Expense ########
        dataExpense = self.openfile(self.pathExpense)
        # Removendo informações desnecessarias
        dataExpense = self.cleanData(dataExpense, True)

        onlyPaidExpense = dataExpense[dataExpense["Coluna"] == "Despesas Pagas"]

        onlyPaidExpenseAndTotal = onlyPaidExpense[
            onlyPaidExpense["Conta"] == "Total Geral da Despesa"
        ]

        uniqueEstados = pd.unique(dataExpense["UF"])

        sumListExpense = []
        statesExpense = []
        for uf in uniqueEstados:
            cidades = onlyPaidExpenseAndTotal[onlyPaidExpenseAndTotal["UF"] == uf]
            soma = 0
            for saldo in cidades["Valor"]:
                if saldo == "Instituição":
                    continue
                fSoma = float(saldo.replace(",", "."))
                soma += fSoma
            statesExpense.append(uf)
            sumListExpense.append(soma)

        # Criar gráficos de gastos
        dataExpenses = {
            'Estados': statesExpense,
            'Gastos': sumListExpense
        }

        dfExpenses = pd.DataFrame(dataExpenses)
        dfExpenses = dfExpenses.sort_values(by='Gastos', ascending=False)

        graphicsExpense = GraphicsImpl(
            dfExpenses['Estados'].to_numpy(),
            dfExpenses['Gastos'].to_numpy(),
            'Despesas Pagas por Estado',
            'Estados',
            'Total de Despesas Pagas'
        )
        generate.generateGraphic(graphicsExpense)

        ######## Budget ########
        dataBudget = self.openfile(self.pathBudget)

        # Removendo informações desnecessarias
        dataBudget = self.cleanData(dataBudget, False)

        onlyPaidBudget = dataBudget[dataBudget["Coluna"] == "Receitas Brutas Realizadas"]

        onlyPaidBudgetAndTotal = onlyPaidBudget[
            onlyPaidBudget["Conta"].str.contains(pat="TOTAL DAS RECEITAS")
        ]

        uniqueEstados = pd.unique(dataBudget["UF"])

        sumListBudget = []
        statesBudget = []
        for uf in uniqueEstados:
            cidades = onlyPaidBudgetAndTotal[onlyPaidBudgetAndTotal["UF"] == uf]
            soma = 0
            for saldo in cidades["Valor"]:
                if saldo == "Instituição":
                    continue
                fSoma = float(saldo.replace(",", "."))
                soma += fSoma
            statesBudget.append(uf)
            sumListBudget.append(soma)

        # Criar gráficos de gastos
        dataBudget = {
            'Estados': statesBudget,
            'Arrecadacao': sumListBudget
        }

        dfBudget = pd.DataFrame(dataBudget)
        dfBudget = dfBudget.sort_values(by='Arrecadacao', ascending=False)

        graphicsBudget = GraphicsImpl(
            dfBudget['Estados'].to_numpy(),
            dfBudget['Arrecadacao'].to_numpy(),
            'Arrecadação por Estado',
            'Estados',
            'Total de Arrecadações'
        )
        generate.generateGraphic(graphicsBudget)

        ######## Saldo das contas do estado ########
        resultStates = []
        cont = 0

        while (len(sumListBudget) > cont):
            resultStates.append(sumListBudget[cont] - sumListExpense[cont])
            cont += 1

        # Criar gráficos de gastos
        dataBalance = {
            'Estados': statesBudget,
            'Saldo': resultStates,
            'Arrecadacao': sumListBudget,
            'Gastos': sumListExpense
        }

        dfBalance = pd.DataFrame(dataBalance)
        dfBalance = dfBalance.sort_values(by='Saldo', ascending=False)

        statesBalance = dfBalance['Estados'].to_numpy()
        valuesBalance = dfBalance['Saldo'].to_numpy()
        valuesBudget = dfBalance['Arrecadacao'].to_numpy()
        valuesExpense = dfBalance['Gastos'].to_numpy()

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
        
        ### Filtrando prefeituras que não estão presentes em ambos os relatorios
        filterExpense = ['Prefeitura Municipal de Bujari - AC', 'Prefeitura Municipal de Uirapuru - GO']
        onlyPaidExpenseAndTotalFiltered = onlyPaidExpenseAndTotal[~onlyPaidExpenseAndTotal["Instituição"].isin(filterExpense)]

        filterBudget = ['Prefeitura Municipal de Nova Lima - MG', 'Prefeitura Municipal de Oliveira - MG', 'Prefeitura Municipal de Piraí do Norte - BA', 'Prefeitura Municipal de Pedro Alexandre - BA']
        onlyPaidBudgetAndTotalFiltered = onlyPaidBudgetAndTotal[~onlyPaidBudgetAndTotal["Instituição"].isin(filterBudget)]

        reportCounties = ReportCounties(
            onlyPaidExpenseAndTotalFiltered["Instituição"].to_numpy(),
            onlyPaidBudgetAndTotalFiltered["Valor"].to_numpy(),
            onlyPaidExpenseAndTotalFiltered["Valor"].to_numpy(),
            onlyPaidBudgetAndTotalFiltered["População"].to_numpy(),
            self.year
        )

        generate.generateReport(reportCounties)
