import gc

keep = True
lista = []
lista2 = []

lista3 = []
lista4 = []


while len(lista2) < 50000000:
    try:
        lista.append("oi")
        lista2.extend(lista)
        print(len(lista2))
    except MemoryError:
        print("MEMORIA EXCEDIDA")  
        keep = False
        break

del lista
del lista2

while len(lista4) < 60000000:
    try:
        lista3.append("oi")
        lista4.extend(lista3)
        print(len(lista4))
    except MemoryError:
        print("MEMORIA EXCEDIDA")
        keep = False
        break
    
del lista3
del lista4

print("\n")
print("STATUS DO GC")
print(gc.get_stats())
print("\n")
print("LIMITES DE COLETA DO GC")
print(gc.get_threshold())
