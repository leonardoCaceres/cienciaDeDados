import numpy as np
import pandas as pd

from Core.dataReaderTemplate import DataReaderTemplate

dataReader = DataReaderTemplate(
    "files/datasets/despesas/despesas2020.csv",
    "files/datasets/receitas/receitas2020.csv",
    2020
)
data2020 = dataReader.initialization()
