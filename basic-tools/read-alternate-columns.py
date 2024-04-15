import pandas as pd

def le_colunas_alternadas(path:str, colunas:list) -> list:
    df = pd.read_excel(path)
    valoresAlternados = []
    
    for index, row in df.iterrows():
        for coluna in colunas:
            valoresAlternados.append(row[coluna])
    
    return valoresAlternados

path = r"data\teste-09042024-152239_-_P12-ContasReceber-H3_Compensacoes_Estorno_de_nota_fiscal_ou_nota_de_credito.xlsx"
colunas = ["Nº Documento  Fatura no SAP", "Nº Documento Adiantamento ou Nota de crédito no SAP"]
le_colunas_alternadas(path, colunas)