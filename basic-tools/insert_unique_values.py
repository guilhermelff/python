valores = []

continua = True

while continua:
    valor = input("insira o valor: ")
    if valor == "":
        continua = False
    else:
        if valor not in valores:
            valores.append(valor)
        else:
            print("valor ja existe")
        
        print(valores)