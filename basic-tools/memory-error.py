import gc

keep = True
lista = []
list2 = []

list3 = []
list4 = []

while len(list2) < 30000000:
    lista.append("oi")
    list2.extend(lista)
    print(len(list2))
    
del list2

while len(list4) < 30000000:
    list3.append("oi")
    list4.extend(list3)
    print(gc.garbage)
    print(len(list4))
