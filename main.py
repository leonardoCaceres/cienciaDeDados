from Core.dataReaderTemplate import DataReaderTemplate

dataReader = DataReaderTemplate(
    "files/datasets/despesas/despesas2020.csv",
    "files/datasets/receitas/receitas2020.csv",
    2020
)
dataReader.initialization()
