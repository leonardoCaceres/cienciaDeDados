import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from report import *

######## Exoense ########
fileExpense = "despesas/despesas.csv"
dataExpense = pd.read_csv(
    fileExpense, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

dataExpense.drop(columns=['Identificador da Conta'], inplace=True)

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

# Personalizando o gráfico
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(statesExpense, sumListExpense, color='skyblue', edgecolor='black')

# Adicionando título e rótulos
ax.set_title('Despesas Pagas por Estado', fontsize=16)
ax.set_xlabel('Estados', fontsize=14)
ax.set_ylabel('Total de Despesas Pagas', fontsize=14)

plt.bar(statesExpense, sumListExpense)
plt.show()

######## Budget ########

fileBudget = "receitas/receitas.csv"
dataBudget = pd.read_csv(
    fileBudget, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

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

# Personalizando o gráfico

resultStates = []
cont = 0

while (len(sumListBudget) > cont):
    resultStates.append(sumListBudget[cont] - sumListExpense[cont])
    cont += 1

fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(statesBudget, resultStates, color='skyblue', edgecolor='black')

# Adicionando título e rótulos
ax.set_title('Arrecadação por Estado', fontsize=16)
ax.set_xlabel('Estados', fontsize=14)
ax.set_ylabel('Total de Arrecadações', fontsize=14)

plt.bar(statesBudget, sumListBudget)
plt.show()

######## Estado das contas do estado ########
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(statesBudget, resultStates, color='skyblue', edgecolor='black')

# Adicionando título e rótulos
ax.set_title('Arrecadação - Despesas', fontsize=16)
ax.set_xlabel('Estados', fontsize=14)
ax.set_ylabel('Total da subtração', fontsize=14)

plt.bar(statesBudget, resultStates)
plt.show()


######## Gerando relatorios nos txt ########
report = Report()
report.createReportStates(statesBudget, sumListBudget, sumListExpense, resultStates)

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
