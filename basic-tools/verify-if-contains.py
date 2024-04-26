colunas = ['teste teste Valor Recebido as onze e meia', 'valorrecebido', 'valor  recebido', 'valor recebido   ']

for coluna in colunas:
    if ("valorrecebido" in coluna.lower().strip().replace(" ", "")):
        print(coluna)


# if any("abc" in s for s in xs):
#     print("oi")