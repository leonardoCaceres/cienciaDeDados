import numpy as np
import pandas as pd

from Core.generate import Generate

from Core.Graphic.Implements.graphics import GraphicsImpl

from Core.Report.Implements.reportCounties import ReportCounties
from Core.Report.Implements.reportStates import ReportStates

from Core.reportStatesAdapter import StatesAdapter
from Core.reportCountiesAdapter import ReportCountiesAdapter


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
        dataFrame.drop(columns=["Identificador da Conta"], inplace=True)
        dataFrame.drop(columns=["Cod.IBGE"], inplace=True)
        if population:
            dataFrame.drop(columns=["População"], inplace=True)

        return dataFrame

    def initialization(self) -> pd.DataFrame:
        ######## Expense ########
        dataExpense = self.openfile(self.pathExpense)
        dataExpense = self.cleanData(dataExpense, True)

        ######## Budget ########
        dataBudget = self.openfile(self.pathBudget)
        dataBudget = self.cleanData(dataBudget, False)

        return self.sumForStates(dataExpense, dataBudget)

    def sumForStates(
        self, dataExpense: pd.DataFrame, dataBudget: pd.DataFrame
    ) -> pd.DataFrame:
        generate = Generate()
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
        dataExpenses = {"Estados": statesExpense, "Gastos": sumListExpense}

        dfExpenses = pd.DataFrame(dataExpenses)
        dfExpenses = dfExpenses.sort_values(by="Gastos", ascending=False)

        graphicsExpense = GraphicsImpl(
            dfExpenses["Estados"].to_numpy(),
            dfExpenses["Gastos"].to_numpy(),
            "Despesas Pagas por Estado",
            "Estados",
            "Total de Despesas Pagas",
        )
        generate.generateGraphic(graphicsExpense)

        onlyPaidBudget = dataBudget[
            dataBudget["Coluna"] == "Receitas Brutas Realizadas"
        ]

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
        dataBudget = {"Estados": statesBudget, "Arrecadacao": sumListBudget}

        dfBudget = pd.DataFrame(dataBudget)
        dfBudget = dfBudget.sort_values(by="Arrecadacao", ascending=False)

        graphicsBudget = GraphicsImpl(
            dfBudget["Estados"].to_numpy(),
            dfBudget["Arrecadacao"].to_numpy(),
            "Arrecadação por Estado",
            "Estados",
            "Total de Arrecadações",
        )
        generate.generateGraphic(graphicsBudget)

        ######## Saldo das contas do estado ########
        resultStates = []
        cont = 0

        while len(sumListBudget) > cont:
            resultStates.append(sumListBudget[cont] - sumListExpense[cont])
            cont += 1

        # Criar gráficos de gastos
        dataBalance = {
            "Estados": statesBudget,
            "Saldo": resultStates,
            "Arrecadacao": sumListBudget,
            "Gastos": sumListExpense,
        }

        dfBalance = pd.DataFrame(dataBalance)
        dfBalance = dfBalance.sort_values(by="Saldo", ascending=False)

        ### Adapter ###
        statesAdapter = StatesAdapter(dfBalance)
        statesAdapter.adapterToReport()

        # ### Filtrando prefeituras que não estão presentes em ambos os relatorios
        # filterExpense = [
        #     "Prefeitura Municipal de Bujari - AC",
        #     "Prefeitura Municipal de Uirapuru - GO",
        # ]
        # onlyPaidExpenseAndTotalFiltered = onlyPaidExpenseAndTotal[
        #     ~onlyPaidExpenseAndTotal["Instituição"].isin(filterExpense)
        # ]

        # filterBudget = [
        #     "Prefeitura Municipal de Nova Lima - MG",
        #     "Prefeitura Municipal de Oliveira - MG",
        #     "Prefeitura Municipal de Piraí do Norte - BA",
        #     "Prefeitura Municipal de Pedro Alexandre - BA",
        # ]
        # onlyPaidBudgetAndTotalFiltered = onlyPaidBudgetAndTotal[
        #     ~onlyPaidBudgetAndTotal["Instituição"].isin(filterBudget)
        # ]

        onlyPaidBudgetAndTotalFiltered, onlyPaidExpenseAndTotalFiltered = (
            self.removeMissingCities(onlyPaidBudgetAndTotal, onlyPaidExpenseAndTotal)
        )

        dataCountie = {
            "Municipios": onlyPaidExpenseAndTotalFiltered["Instituição"].to_numpy(),
            "Arrecadacao": onlyPaidBudgetAndTotalFiltered["Valor"].to_numpy(),
            "Gastos": onlyPaidExpenseAndTotalFiltered["Valor"].to_numpy(),
            "Populacao": onlyPaidBudgetAndTotalFiltered["População"].to_numpy(),
        }

        dfBCountie = pd.DataFrame(dataCountie)
        reportCountiesAdapter = ReportCountiesAdapter(dfBCountie, self.year)
        reportCountiesAdapter.adapterToReport()

        return dfBCountie

    def removeMissingCities(self, receitas, despesas):
        ids_comuns = pd.merge(
            receitas[["Instituição"]],
            despesas[["Instituição"]],
            on="Instituição",
            how="inner",
        )["Instituição"]
        # Filtrando os DataFrames para manter apenas os valores que estão na interseção
        receitas_filtrado = receitas[
            receitas["Instituição"].isin(ids_comuns)
        ].reset_index(drop=True)
        despesas_filtrado = despesas[
            despesas["Instituição"].isin(ids_comuns)
        ].reset_index(drop=True)
        return receitas_filtrado, despesas_filtrado
