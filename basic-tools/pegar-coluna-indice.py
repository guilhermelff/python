import pandas as pd 

pathPlanilha = "teste.xlsx"

#ler coluna pelo indice

df = pd.read_excel(pathPlanilha)
print(df.iloc[0, 0])