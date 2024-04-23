import os
import shutil
 
destino = r'C:\Users\guilh\OneDrive\Documents\GitHub\python\basic-tools\teste3.xlsx'
 
# destination file path
fonte = r'C:\Users\guilh\OneDrive\Documents\GitHub\python\basic-tools\teste2.xlsx'

fonte2 = r'C:\Users\guilh\OneDrive\Documents\GitHub\python\basic-tools\teste3.xlsx'

destino2 = r'C:\Users\guilh\OneDrive\Documents\GitHub\python\basic-tools\teste4.xlsx'

# copia
shutil.copyfile(fonte, destino)

# renomeia
os.rename(fonte2, destino2)
