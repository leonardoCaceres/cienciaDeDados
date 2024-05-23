import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

## Despesas
fileExpense = "despesas/despesas.csv"
dataExpense = pd.read_csv(
    fileExpense, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

uniqueNamesExpense = pd.unique(dataExpense["Instituição"])

onlyPaidExpense = dataExpense[dataExpense["Coluna"] == "Despesas Pagas"]

onlyPaidExpenseAndTotal = onlyPaidExpense[
    onlyPaidExpense["Conta"] == "Total Geral da Despesa"
]

uniqueEstados = pd.unique(dataExpense["UF"])

sumList = []
states = []
for uf in uniqueEstados:
    cidades = onlyPaidExpenseAndTotal[onlyPaidExpenseAndTotal["UF"] == uf]
    soma = 0
    for saldo in cidades["Valor"]:
        if saldo == "Instituição":
            continue
        fSoma = float(saldo.replace(",", "."))
        soma += fSoma
    states.append(uf)
    sumList.append(soma)

# Personalizando o gráfico
fig, ax = plt.subplots(figsize=(12, 6))

bars = ax.bar(states, sumList, color='skyblue', edgecolor='black')

# Adicionando título e rótulos
ax.set_title('Despesas Pagas por Estado', fontsize=16)
ax.set_xlabel('Estados', fontsize=14)
ax.set_ylabel('Total de Despesas Pagas', fontsize=14)

plt.bar(states, sumList)
plt.show()

## Budget
fileBudget = "receitas/receitas.csv"
dataBudget = pd.read_csv(
    fileBudget, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
)

uniqueNamesBudget = pd.unique(dataBudget["Instituição"])

onlyPaidBudget = dataBudget[dataBudget["Coluna"] == "Receitas Brutas Realizadas"]

onlyPaidBudgetAndTotal = onlyPaidBudget[
    onlyPaidBudget["Conta"].str.contains(pat="TOTAL DAS RECEITAS")
]

uniqueEstados = pd.unique(dataBudget["UF"])

sumList = []
states = []
for uf in uniqueEstados:
    cidades = onlyPaidBudgetAndTotal[onlyPaidBudgetAndTotal["UF"] == uf]
    soma = 0
    for receita in cidades["Valor"]:
        if receita == "Instituição":
            continue
        fSoma = float(receita.replace(",", "."))
        soma += fSoma
    states.append(uf)
    sumList.append(soma)

plt.bar(states, sumList)
plt.show()


"""
for index in range(0, len(onlyPaid)):
    if onlyPaid[index] == True:
        print(data.loc[index])
"""

"""
onlyPaid = data["Coluna"].str.contains(pat="Despesas Pagas")
uniqueNames = pd.unique(onlyPaid["Instituição"])
print(uniqueNames.shape)

onlyPaidAndTotal = onlyPaid[onlyPaid["Conta"] == "Total Geral da Despesa"]

uniqueNames = pd.unique(onlyPaidAndTotal["Instituição"])
print(uniqueNames.shape)
# print(onlyPaidAndTotal)

# faltando = data[data]
"""
