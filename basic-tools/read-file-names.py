from os import listdir
from os.path import isfile, join

mypath = r'C:\Users\guilh\OneDrive\Documents\GitHub\python\basic-tools\data'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


anterior_eh_h = False
achou_h3 = False
for filename in onlyfiles:
    
    descricao_h3 = ""

    for letra in filename[:-5]:

        if (achou_h3 == True):
            descricao_h3 += letra.lower()

        if (achou_h3 == False):
            
            if (letra.lower() == "3" and anterior_eh_h):
                achou_h3 = True

            if (letra.lower() == "h"):
                anterior_eh_h = True
                continue
            else:
                anterior_eh_h = False

        

    achou_h3 = False
    anterior_eh_h = False
        
    print(descricao_h3)