import numpy as np
import pandas as pd

from report import *
from graphics import *

######## Expense ########
fileExpense = "despesas/despesas.csv"
dataExpense = pd.read_csv(
    fileExpense, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

# Removendo informações desnecessarias
dataExpense.drop(columns=['Identificador da Conta'], inplace=True)
dataExpense.drop(columns=['População'], inplace=True)

uniqueNamesExpense = pd.unique(dataExpense["Instituição"])

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

graphics = Graphics()
graphics.createGraphics(
    dfExpenses['Estados'].to_numpy(),
    dfExpenses['Gastos'].to_numpy(),
    'Despesas Pagas por Estado',
    'Estados',
    'Total de Despesas Pagas'
)

######## Budget ########

fileBudget = "receitas/receitas.csv"
dataBudget = pd.read_csv(
    fileBudget, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

# Removendo informações desnecessarias
dataBudget.drop(columns=['Identificador da Conta'], inplace=True)

uniqueNamesBudget = pd.unique(dataBudget["Instituição"])

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
    for receita in cidades["Valor"]:
        if receita == "Instituição":
            continue
        fSoma = float(receita.replace(",", "."))
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

graphics.createGraphics(
    dfBudget['Estados'].to_numpy(),
    dfBudget['Arrecadacao'].to_numpy(),
    'Arrecadação por Estado',
    'Estados',
    'Total de Arrecadações'
)

######## Saldo das contas do estado ########
resultStates = []
cont = 0

while (len(sumListBudget) > cont):
    resultStates.append(sumListBudget[cont] - sumListExpense[cont])
    cont += 1

# Criar gráficos de gastos
dataBalance = {
    'Estados': statesBudget,
    'Saldo': resultStates
}

dfBalance = pd.DataFrame(dataBalance)
dfBalance = dfBalance.sort_values(by='Saldo', ascending=False)

statesBalance = dfBalance['Estados'].to_numpy()
valuesBalance = dfBalance['Saldo'].to_numpy()

graphics.createGraphics(
    statesBalance,
    valuesBalance,
    'Saldo dos Estado',
    'Estados',
    'Total do Saldo'
)


######## Gerando relatorios nos txt ########
report = Report()
report.createReportStates(statesBalance, sumListBudget, sumListExpense, valuesBalance)

### Filtrando prefeituras que não estão presentes em ambos os relatorios
filterExpense = ['Prefeitura Municipal de Bujari - AC', 'Prefeitura Municipal de Uirapuru - GO']
onlyPaidExpenseAndTotalFiltered = onlyPaidExpenseAndTotal[~onlyPaidExpenseAndTotal["Instituição"].isin(filterExpense)]

filterBudget = ['Prefeitura Municipal de Nova Lima - MG', 'Prefeitura Municipal de Oliveira - MG', 'Prefeitura Municipal de Piraí do Norte - BA', 'Prefeitura Municipal de Pedro Alexandre - BA']
onlyPaidBudgetAndTotalFiltered = onlyPaidBudgetAndTotal[~onlyPaidBudgetAndTotal["Instituição"].isin(filterBudget)]

profit = report.calculateCountiesProfit(
    onlyPaidBudgetAndTotalFiltered["Valor"].to_numpy(), 
    onlyPaidExpenseAndTotalFiltered["Valor"].to_numpy()
)

### Criado novo dataframe com as informações que queremos utilizar
dataCounties = {
    'Municipios': onlyPaidExpenseAndTotalFiltered["Instituição"].to_numpy(),
    'Gastos': onlyPaidExpenseAndTotalFiltered["Valor"].to_numpy(),
    'Arrecadacao': onlyPaidBudgetAndTotalFiltered["Valor"].to_numpy(),
    'Populacao': onlyPaidBudgetAndTotalFiltered["População"].to_numpy(),
    'Lucro' : profit
}

dfCounties = pd.DataFrame(dataCounties)
dfCounties = dfCounties.sort_values(by='Lucro', ascending=False)

# Calculando os quartis
q1 = dfCounties['Lucro'].quantile(0.25)
q2 = dfCounties['Lucro'].quantile(0.50)
q3 = dfCounties['Lucro'].quantile(0.75)

# Adicionando a coluna de quartil com o valor do quartil correspondente
dfCounties['Quartil'] = dfCounties['Lucro'].apply(lambda x: report.determinar_quartil(x, q1, q2, q3))

counties = dfCounties["Municipios"].to_numpy()
countiesExpense = dfCounties["Gastos"].to_numpy()
countiesBudget = dfCounties["Arrecadacao"].to_numpy()
countiesPopulation = dfCounties["Populacao"].to_numpy()
countiesQuartis = dfCounties['Quartil'].to_numpy()
countiesProfit = report.calculateCountiesProfit(countiesBudget, countiesExpense)

report.createReportCounties(
    counties,
    countiesBudget,
    countiesExpense,
    countiesPopulation,
    countiesProfit,
    countiesQuartis
)
