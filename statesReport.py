class StatesReport:
    def __init__(self, states, budget, expense, result):
        self.state = states
        self.budget = budget
        self.expense = expense
        self.result = result
    
    def createReport(self):
        report = 'report.txt'
        try:
            file = open(report, 'r', encoding='utf-8')
            line = file.readlines()
            cont = 0
            while len(self.state) > cont:
                percentage = (100*self.result[cont])/self.budget[cont]
                line.append(
                    f"{self.state[cont]} \n"
                    + f"Arrecadação: {self.budget[cont]:.2f} \n"
                    + f"Gastos: {self.expense[cont]:.2f} \n"
                    + f"Lucro: {self.result[cont]:.2f} "
                    + f"({percentage:.2f}%)\n"
                    + '---------------------------------- \n')
                cont += 1
            file = open(report, 'w', encoding='utf-8')
            file.writelines(line)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        else:
            print('Relatorio gerado com sucesso!')
        
        finally:
            file.close()
        