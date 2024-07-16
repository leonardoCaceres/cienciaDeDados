import os

import numpy as np
import pandas as pd

from generate import Generate

from Graphic.Implements.graphics import GraphicsImpl

from Report.Implements.reportCounties import ReportCounties
from Report.Implements.reportStates import ReportStates

def openfile(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, path)
    data = pd.read_csv(
    file_path, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
    )
    return data

def  calculateSumStates(uniqueEstados, onlyPaidAndTotal):
    sumList = []
    states = []
    for uf in uniqueEstados:
        cidades = onlyPaidAndTotal[onlyPaidAndTotal["UF"] == uf]
        soma = 0
        for saldo in cidades["Valor"]:
            if saldo == "Instituição":
                continue
            fSoma = float(saldo.replace(",", "."))
            soma += fSoma
        states.append(uf)
        sumList.append(soma)
    return sumList, states

generate = Generate()

######## Expense ########
dataExpense = openfile("despesas/despesas.csv")
# Removendo informações desnecessarias
dataExpense.drop(columns=['Identificador da Conta'], inplace=True)
dataExpense.drop(columns=['Cod.IBGE'], inplace=True)
dataExpense.drop(columns=['População'], inplace=True)

uniqueNamesExpense = pd.unique(dataExpense["Instituição"])

onlyPaidExpense = dataExpense[dataExpense["Coluna"] == "Despesas Pagas"]

onlyPaidExpenseAndTotal = onlyPaidExpense[
    onlyPaidExpense["Conta"] == "Total Geral da Despesa"
]

uniqueEstados = pd.unique(dataExpense["UF"])

sumListExpense, statesExpense = calculateSumStates(uniqueEstados, onlyPaidExpenseAndTotal)

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
dataBudget = openfile("receitas/receitas.csv")

# Removendo informações desnecessarias
dataBudget.drop(columns=['Identificador da Conta'], inplace=True)
dataBudget.drop(columns=['Cod.IBGE'], inplace=True)

uniqueNamesBudget = pd.unique(dataBudget["Instituição"])

onlyPaidBudget = dataBudget[dataBudget["Coluna"] == "Receitas Brutas Realizadas"]

onlyPaidBudgetAndTotal = onlyPaidBudget[
    onlyPaidBudget["Conta"].str.contains(pat="TOTAL DAS RECEITAS")
]

uniqueEstados = pd.unique(dataBudget["UF"])

sumListBudget, statesBudget = calculateSumStates(uniqueEstados, onlyPaidBudgetAndTotal)

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
reportStates = ReportStates(statesBalance, valuesBudget, valuesExpense, valuesBalance)
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
    onlyPaidBudgetAndTotalFiltered["População"].to_numpy()
)

generate.generateReport(reportCounties)
