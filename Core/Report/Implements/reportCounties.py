from typing import List, Dict, Any
import numpy as np

from Report.reportInterface import ReportInterface

class ReportCounties(ReportInterface):

    def __init__(
            self,
            counties: np.ndarray,
            budget: np.ndarray,
            expense: np.ndarray,
            population: np.ndarray,
        ):
        self.counties = counties
        self.budget = budget
        self.expense = expense
        self.population = population
    
    def createReport(self) -> None:
        report = 'files/reports/reportCounties.txt'
        try:
            with open(report, 'w+', encoding='utf-8') as file:
                countiesOrdened = self.ordenarCounties()
                counties = countiesOrdened['Municipios']
                expense = countiesOrdened['Gastos']
                budget = countiesOrdened['Arrecadacao']
                population = countiesOrdened['Populacao']
                balance = countiesOrdened['Saldo']

                # Calculando os quartis
                q3 = balance[int(len(balance)/4)]
                q2 = balance[int(len(balance)/2)]
                q1 = balance[int(3*(len(balance)/4))]
                print(q1)
                print(q2)
                print(q3)

                cont = 0
                prejuizo = 0
                lucro = 0
                lines = []
                while len(counties) > cont:
                    PIB = float(budget[cont].replace(",", ".")) / float(population[cont])
                    if balance[cont] > 0:
                        lucro += 1
                    elif balance[cont] < 0:
                        prejuizo += 1
                    lines.append(
                        f"{counties[cont]} \n"
                        + f"Arrecadação: {budget[cont]} \n"
                        + f"Gastos: {expense[cont]} \n"
                        + f"Saldo orçamentário: {balance[cont]:.2f} \n"
                        + f"Arrecadação per capita do município: {PIB:.2f} \n"
                        + f"Posição do município: {self.determinar_quartil(balance[cont], q1, q2, q3)} \n"
                        + '---------------------------------- \n'
                    )
                    cont += 1
                lines.append(f"Total de municípios com superávit Orçamentário: {lucro} \n")
                lines.append(f"Total de municípios com déficit Orçamentário: {prejuizo} \n")
                file.writelines(lines)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        else:
            print('Relatório dos municípios gerado com sucesso!')
    
    def calculateBalance(self, budget: List[str], expense: List[str]) -> List[float]:
        result = []
        
        for b, e in zip(budget, expense):
            result.append(float(b.replace(",", ".")) - float(e.replace(",", ".")))
        
        return result

    
    def determinar_quartil(self, valor: float, q1: float, q2: float, q3: float) -> str:
        if valor <= q1:
            return 'Entre os 25% piores'
        elif valor <= q2:
            return 'Entre os 25 e os 50%'
        elif valor <= q3:
            return 'Entre os 50 e os 75%'
        else:
            return 'Entre os 25% melhores'
    
    def ordenarCounties(self) -> Dict[str, Any]:
        municipios = self.counties.tolist()
        gastos = self.expense.tolist()
        arrecadacao = self.budget.tolist()
        populacao = self.population.tolist()
        saldo = self.calculateBalance(self.budget.tolist(), self.expense.tolist())

        # Unindo os dados para ordenação
        combined = list(zip(saldo, populacao, municipios, gastos, arrecadacao))

        # Ordenando pelo saldo em ordem decrescente
        combined_sorted = sorted(combined, key=lambda x: x[0], reverse=True)

        saldoSorted, populacao_sorted, municipios_sorted, gastos_sorted, arrecadacao_sorted = zip(*combined_sorted)

        dataCounties_sorted = {
            'Municipios': municipios_sorted,
            'Gastos': gastos_sorted,
            'Arrecadacao': arrecadacao_sorted,
            'Populacao': populacao_sorted,
            'Saldo': saldoSorted
        }
        
        return dataCounties_sorted
