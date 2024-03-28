import json
import pandas as pd
import os

#insira caminho do excel aqui
caminhoArquivo = rf'..\arquivos\excel\27032024-093055_-_P12-H1-Contas_Receber-Identificacoes-2900-20240327_072232.xlsx'

#lê excel num dataframe e retira linhas totalmente nulas
df = pd.read_excel(caminhoArquivo, index_col=0, skiprows=1)
df = df[df.index.notnull()]

#cria pasta para salvar os arquivos json
if not os.path.exists('./json'):
    os.mkdir('./json')

#acessa cada coluna
for col in df.columns:
    #transforma cada coluna num json e salva num dicionario python, com a chave igual ao nome da coluna
    str = df[col].to_json(orient='columns')
    dict = {col: str}
   
    #cria um novo nome para a coluna, substitui '/' por '-' para não dar erro na hora de salvar o arquivo
    novoNome = col.replace('/', '-')

    #especifica coluna que não vai ser salva
    if (novoNome == 'Sobra de Troco - BH'):
        continue

    #salva o arquivo no diretório json
    with open(rf'json/{novoNome}.json', 'w') as fp:
        json.dump(dict, fp)
