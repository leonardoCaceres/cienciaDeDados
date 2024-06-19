class Report:
    def createReportStates(self, states, budget, expense, result):
        report = 'reportStates.txt'
        try:
            file = open(report, 'w+', encoding='utf-8')
            line = file.readlines()
            cont = 0
            while len(states) > cont:
                percentage = (100*result[cont])/budget[cont]
                line.append(
                    f"{states[cont]} \n"
                    + f"Arrecadação: {budget[cont]:.2f} \n"
                    + f"Gastos: {expense[cont]:.2f} \n"
                    + f"Saldo orçamentario: {result[cont]:.2f} "
                    + f"({percentage:.2f}%) da arrecadação\n"
                    + '---------------------------------- \n')
                cont += 1
            file.writelines(line)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        else:
            print('Relatorio dos estados gerado com sucesso!')
        
        finally:
            file.close()
    
    def createReportCounties(
            self,
            counties,
            countiesBudget,
            countiesExpense,
            population,
            countiesProfit,
            countiesQuartis
        ):

        report = 'reportCounties.txt'
        try:
            file = open(report, 'w+', encoding='utf-8')
            line = file.readlines()
            cont = 0
            
            prejuizo = 0
            lucro = 0

            while len(counties) > cont:
                PIB = float(countiesBudget[cont].replace(",", "."))/float(population[cont])
                if (countiesProfit[cont] > 0):
                    lucro += 1
                elif (countiesProfit[cont] < 0):
                    prejuizo += 1
                line.append(
                    f"{counties[cont]} \n"
                    + f"Arrecadação: {countiesBudget[cont]} \n"
                    + f"Gastos: {countiesExpense[cont]} \n"
                    + f"Saldo orçamentario: {countiesProfit[cont]:.2f} \n"
                    + f"Arecadação per capta do municipio: {PIB:.2f} \n"
                    + f"Posição do municipio: {countiesQuartis[cont]} \n"
                    + '---------------------------------- \n')
                cont += 1
            line.append(f"Total de municipios com superávit Orçamentário: {lucro} \n")
            line.append(f"Total de municipios com déficit Orçamentário: {prejuizo} \n")
            file.writelines(line)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        else:
            print('Relatorio dos municipios gerado com sucesso!')
        
        finally:
            file.close()
    
    def calculateCountiesProfit(self, countiesBudget, countiesExpense):
        cont = 0
        result = []
        
        while len(countiesBudget) > cont:
            result.append(float(countiesBudget[cont].replace(",", ".")) - float(countiesExpense[cont].replace(",", ".")))
            cont += 1
        
        return result
    
    def determinar_quartil(self, valor, q1, q2, q3):
        if valor <= q1:
            return 'Entre os 25% piores'
        elif valor <= q2:
            return 'Entre os 25 e os 50%'
        elif valor <= q3:
            return 'Entre os 50 e os 75%'
        else:
            return 'Entre os 25% melhores'
        