from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import time
import SRSCloud_Integration as srsc

def main():
    if len(sys.argv) > 1:
        filaId = sys.argv[1]
    else:
        filaId = None

with open(f"C:\Testes SRS\srs.json") as json_data_file:
        config_json = json.load(json_data_file)

workflowAlias = config_json["srscloud_config"]["workflowAlias"]
    tarefaAlias = 'nc'
    maquina = 'Maquina_Paulo'#prod

inicio = json.loads(srsc.execucaoIniciar(tarefa=tarefaAlias))
    #easygui.msgbox(f'{inicio}')
    execucaoId = inicio['ExecucaoId']

while FilaItem['Autorizado'] == True:
            with open('ambiente.txt', 'a') as file:file.write(f"\n Ambiente = {FilaItem['Fila'][0]}")
            fila = FilaItem['Fila'][0]
            filaId = fila['FilaId']
            parametros = json.loads(fila['ParametrosEntrada'])
            browser = parametros['browser']
            ambiente = Ambiente(parametros['ambiente'])
            with open('ambiente.txt', 'a') as file:file.write(f"\n Ambiente = {ambiente}")



#verifica se o CEP tem oito números
def cep_eh_valido(cep):
       
        if (cep.isnumeric()):
            if len(cep) == 8:
                padrao_cep = re.compile(r'(\d){5}(\d){3}')

                match = padrao_cep.match(cep)

                return True
        else:
            return False


#lê a planilha de CEPs em um data frame
enderecosDf = pd.read_excel('enderecos.xlsx')


#abre uma instancia do Firefox e entra no site de buscas dos correios
driver = webdriver.Firefox()
driver.get("https://buscacepinter.correios.com.br/app/endereco/index.php")


#para cada linha de CEP na planilha, verifica se o CEP está no formato certo, depois verifica se o site dos correios retorna um endereço, se não retornar faz uma nova busca com um novo CEP
print("Buscando os CEPs...")
for index, row in enderecosDf.iterrows():

	if filaId != None:
            FilaItem = json.loads(srsc.filaProximoNomeada(execucaoId=execucaoId,filaId=filaId))
        else:
            FilaItem = json.loads(srsc.filaProximo(execucaoId=execucaoId))

	if FilaItem['Autorizado'] != True:
            #easygui.msgbox(f'{FilaItem}')
            entrada = {"browser":"chrome","ambiente": "prod"}
            srsc.filaInserir(referencia='testeFila',entrada=json.dumps(entrada))
            FilaItem = json.loads(srsc.filaProximo(execucaoId=execucaoId))
            #easygui.msgbox(f'{FilaItem}')

    cep = row['cep'];
    cep = str(cep)

    if cep_eh_valido(cep):

        #digita o CEP e clica em buscar
        driver.find_element(By.XPATH, '//*[@id="endereco"]').send_keys(cep)
        driver.find_element(By.XPATH, '//*[@id="btn_pesquisar"]').click()
        time.sleep(3)

        #verifica se CEP existe
        try:
            rua = driver.find_element(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[1]').text
            bairro = driver.find_element(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[2]').text
            local = driver.find_element(By.XPATH, '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[3]').text

        #salva o endereço no data frame
            enderecosDf.loc[index, 'rua'] = str(rua)
            enderecosDf.loc[index, 'bairro'] = str(bairro)
            enderecosDf.loc[index, 'local'] = str(local)
    
        except:
            #clica em nova busca
            driver.find_element(By.XPATH, '//*[@id="btn_nbusca"]').click()
            time.sleep(3)
            continue

        #clica em nova busca
        novaBusca = driver.find_element(By.XPATH, '//*[@id="btn_nbusca"]')
        novaBusca.click()
        time.sleep(3)


#salva o data frame no arquivo excel
print("Salvando arquivo...")
enderecosDf.to_excel('enderecos.xlsx',index=False)
print("Salvo com sucesso")
