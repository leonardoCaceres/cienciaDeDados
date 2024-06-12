class StatesReport:
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
                    + f"Lucro: {result[cont]:.2f} "
                    + f"({percentage:.2f}%)\n"
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
    
    def createReportCounties(self, counties, countiesBudget, countiesExpense):
        report = 'reportCounties.txt'
        try:
            file = open(report, 'w+', encoding='utf-8')
            line = file.readlines()
            cont = 0
            
            prejuizo = 0
            lucro = 0

            while len(counties) > cont:
                result = float(countiesBudget[cont].replace(",", ".")) - float(countiesExpense[cont].replace(",", "."))
                if (result > 0):
                    lucro += 1
                elif (result < 0):
                    prejuizo += 1
                line.append(
                    f"{counties[cont]} \n"
                    + f"Arrecadação: {countiesBudget[cont]} \n"
                    + f"Gastos: {countiesExpense[cont]} \n"
                    + f"Lucro: {result:.2f} \n"
                    + '---------------------------------- \n')
                cont += 1
            file.writelines(line)
            print(f"Número de municipios que dão prejuizo: {prejuizo}")
            print(f"Número de municipios que tem lucro: {lucro}")
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        else:
            print('Relatorio dos municipios gerado com sucesso!')
        
        finally:
            file.close()
        