import json
import requests
import os
from urllib3.util import parse_url, Url
from urllib.parse import quote
import inspect
import base64

"""
#Versão 2024.01.31
"""

#vincular o arquivo srs.json onde os parametros de acesso devem ser definidos
with open("srs.json") as json_data_file:
    config_json = json.load(json_data_file)

SRShost = config_json["srscloud_config"]["url"]
token = config_json["srscloud_config"]["token"]
proxyConfig = config_json["proxy"]
usarProxy = proxyConfig["usarProxy"]

#biblioteca ajustada para executar com uma unica tarefa, 
#para multimplas tarefas, precisa voltar os parametros comentados
workflow_unico = config_json["srscloud_config"]["workflowAlias"]
tarefa_unica = config_json["srscloud_config"]["tarefaAlias"]
maquina_unica = config_json["srscloud_config"]["maquina"]

#Lista de Status Para fila e Execucao
"""
--- Use o campo Status como referencia, em alguns casos voce pode usar o StatusId ---
           StatusID	Status	    Descricao
StatusFila	0	    NaFila	    Aguardando
StatusFila	1	    FilaExec	Em execução
StatusFila	2	    FilaOk	    Finalizado com Sucesso
StatusFila	3	    FilaErro	Finalizado com erro
StatusFila	4	    Recolocar	Realocado
StatusFila	5	    Remover	    Removido

        	   StatusId	Status	    Descricao
StatusExecucao	1	    Inicio	    Inicio
StatusExecucao	2	    Log	        Log
StatusExecucao	3	    Alerta	    Alerta
StatusExecucao	4	    Ok	        Encerrado com Sucesso
StatusExecucao	5	    Erro	    Encerrado com Erro
StatusExecucao	6	    Timeout	    Encerrado porTimeout
StatusExecucao	7	    Parar	    Execucao cancelada
"""

# Funçoes de comunicação com as APIs do SRS
 
def formatar_arquivo(arquivo):#formata o arquivo para enviar
    retorno = {}
    nomeArquivo = os.path.basename(arquivo).lower()
    with open(arquivo, "rb") as f: arquivo64 = base64.b64encode(f.read())
    
    arquivo64 = str(arquivo64)[2:-1] #transforma binario em str
    retorno = {'filename':nomeArquivo, 'base64': arquivo64}
    return retorno

def salvar_arquivo(parametro, pasta):#recebe o arquivo em bytes e salva na pasta desejada
    arquivo64_decodificado = base64.b64decode(parametro['base64'])
    nomeArquivo = f"{pasta}/{parametro['filename']}"
    with open(nomeArquivo, "wb") as f:
        f.write(arquivo64_decodificado)
    return nomeArquivo

def proxy():#configurações de proxy
    url_dict = parse_url(proxyConfig["server"])._asdict()
    url_dict['auth'] = proxyConfig["user"] + ':' + quote(proxyConfig["pass"], '')
    urlProxy =  Url(**url_dict).url
    return {'http': urlProxy, 'https': urlProxy}

# controle de execução
def execucaoIniciar(workflow=workflow_unico, tarefa=tarefa_unica, maquina=maquina_unica): 
    """#Retorno:
    {"Autorizado": true,
    "ExecucaoId": "5aa2bbfa-bbc2-4530-8ebd-d2df63623b4b",
    "Mensagem": "",
    "Parametros": [
        {
        "AlteradoPorAPI": 0,
        "NomeParametro": "localPlanilha",
        "TipodadoId": "1",
        "ValorParametro": "c:/planilha.xlsx"
        }
    ]} 

    #Observações: 
    #- Lembrar de cadastrar o workflow, tarefa, maquina e token de usuario no Portal 
    #- workflow e tarefa a referencia é o campo Alias do Portal 
    #- maquina é o Nome da Maquina do Portal 
    #- token é o token de usuario cadastrado no seu perfil 
    """
    entrada = {'token':token,
        'workflow':workflow,
        'tarefa':tarefa,
        'nomeMaquina':maquina,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}execucao/iniciar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}execucao/iniciar", data=entrada)
    return response.text

def log(execucaoId, statusId, mensagem, arquivo='none'):
    if arquivo: 
        arquivo64 = formatar_arquivo(arquivo)
        arquivo64 = json.dumps(arquivo64)
    else: arquivo64 = {}

    entrada = {'token':token,
        'statusId':statusId, #(2=mensagem de andamento, 3=alerta)
        'descricao':mensagem,
        'execucaoId':execucaoId,
        'arquivo': arquivo64,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}execucao/log", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}execucao/log", data=entrada)
    return response.text

def parametroAtualizar(parametro, valor, workflow=workflow_unico, tarefa=tarefa_unica):
    """#voce pode criar parametros com permissão de alteração pelo robo, 
       #utilize esta função para alterar este parametro"""
    entrada={'token': token,
        'workflow': workflow,
        'tarefa': tarefa,
        'parametro': parametro,
        'valor': valor,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}tarefa/parametro", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}tarefa/parametro", data=entrada)
    return response.text

def execucaoFinalizar(execucaoId, status='ok', mensagem='Execução finalizada'):
    """#para registrar um erro use status='erro'"""
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'status': status,
        'descricao':mensagem,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}execucao/finalizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}execucao/finalizar", data=entrada)
    return response.text

# controle de credenciais
def credencialObter(execucaoId, sistema):
    """Retorno:
    {"Autorizado": true,
    "Credencial": {
        "CredencialId": "28d23acb-2739-4498-9e23-9e0decd154b9",
        "EmExecucao": null,
        "ExpiraEm": "Tue, 26 Dec 2023 00:00:00 GMT",
        "Expirada": 0,
        "GerarSenha": 0,
        "NomeCredencial": "RoboAdm",
        "ResponsavelCelular": "",
        "ResponsavelEmail": "",
        "ResponsavelNome": ""
    },
    "CredencialParametro": {
        "Empresa": "Automate",
        "Senha": "batatafrita",
        "Usuario": "Christian"
    },
    "Mensagem": "Credencial RoboAdm do sistema SAP concedida",
    "Sistema": {
        "AcessoExclusivo": 0,
        "Autorizado": true,
        "Caminho": "http://localhost:123/sap",
        "Corporativo": 1,
        "NomeSistema": "SAP",
        "RespNegEmail": "marcelo.favero@automate.com.br",
        "RespNegNome": "Marcelo Favero",
        "RespNegTelefone": "11973097301",
        "RespTecEmail": "herminio.pereira@automate.com.br",
        "RespTecNome": "Herm\u00ednio Pereira",
        "RespTecTelefone": "11998725567",
        "SistemaId": "1",
        "TipoAcesso": "Login e Senha",
        "TipoAcessoId": "1",
        "TipoInterface": "WebBrowser",
        "TipoInterfaceId": "1"
    }}
    """
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'sistema':sistema,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}credencial/obter", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}credencial/obter", data=entrada)
    return response.text

def credencialAlterar(execucaoId, sistema, credencialId, expiraEm, parametro, valorAntigo, valorNovo, ativo=1):
    """#utilize esta função para atualizar o status (1=ativo/0=inativo), senhas e data da expiração das credenciais"""
    entrada={'token': token,
        'execucaoId': execucaoId,
        'sistema': sistema,
        'credencialId': credencialId,
        'ativo': ativo,#1=ativo, 0=inativo
        'expiraEm': expiraEm,
        'parametro': parametro,
        'valorAntigo': valorAntigo,
        'valorNovo': valorNovo,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}credencial/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}credencial/atualizar", data=entrada)
    return response.text

# controle de fila
def filaInserir(referencia, entrada, workflow=workflow_unico, tarefa=tarefa_unica, execucaoId = None): 
    entrada={'token': token,
        'workflow': workflow,
        'tarefa': tarefa,
        'referencia': referencia,
        'parametroEntrada': entrada,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }
    if execucaoId: entrada['execucaoId'] = execucaoId

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada)
    return response.text

def filaInserirExecutando(execucaiId, referencia, entrada, workflow=workflow_unico, tarefa=tarefa_unica):
    """#a diferença deste inserir é que o item de fila já retorna para voce como em execução, não é necessário pedir proximo"""
    entrada={'token': token,
        'workflow': workflow,
        'tarefa': tarefa,
        'referencia': referencia,
        'parametroEntrada': entrada,
        'execucaoId': execucaiId,
        'status': 'EmExecucao',
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada)
    return response.text

def filaInserirLote(lote, workflow=workflow_unico, tarefa=tarefa_unica, execucaoId = None):
    """#voce pode inserir um conjunto de itens de uma unica vez
    #lote: [{'referencia': 'valor', 'parametroEntrada':[{'parametro':'valor', 'parametro': 'valor'}] }]"""
    entrada={'token': token,
        'workflow': workflow,
        'tarefa': tarefa,
        'lote': lote,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }
    if execucaoId: entrada['execucaoId'] = execucaoId

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/inserir", data=entrada)
    return response.text

def filaProximo(execucaoId, qtd=1):#retorna o proximo item da fila, voce pode alterar a quantidade para trazer mais de 1
    """Resultado:
    { "Autorizado": true,
    "Fila": [
        {
        "DataInclusao": "Fri, 01 Sep 2023 11:03:42 GMT",
        "DataUltimoStatus": "Mon, 29 Jan 2024 16:45:46 GMT",
        "FilaId": "409ed1a7-eaf7-4dda-b46e-5c2f7b019b5a",
        "Lote": "e842bf77-5b4e-4d78-b501-57b8e5e9432f",
        "Mensagem": "Acionamento manual pelo site",
        "ParametrosEntrada": "{\"Email\": \"christian.marcondes@automate.com.br\", \"Nome\": \"Christian\"}",
        "Realocado": 0,
        "Referencia": "Execucao Manual"
        }
    ],
    "Mensagem": ""
    }
    #A fila vem em um array pois pode vir mais de um registro no retorno de lote 
    #Os ParametrosEntrada são um json dentro de um json, precisa converter o resultado
    """
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'lote': qtd,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/proximo", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/proximo", data=entrada)
    return response.text

def filaProximoNomeada(execucaoId, filaId):
    """#retorna um item específico da fila, muito usado para receber execucao manual"""
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'filaId': filaId,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/proximo", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/proximo", data=entrada)
    return response.text

def filaAtualizar(execucaoId, filaId, saida, statusId, proximo=0, mensagem='Fila atualizada com sucesso'):
    #atualizar generico
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'filaId':filaId,
        'statusId': statusId, #(0=aguardando, 1=em execucao, 2=encerrado com sucesso, 3=encerrado com erro)
        'Mensagem':mensagem,
        'parametroSaida': saida,
        'proximo':proximo,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada)
    return response.text

def filaAtualizarLote(execucaoId, lote):
    """#atualiza vário registros ao mesmo tempo (todos os itens atualizados devem, obrigatoriamente, 
    #estar em status 1(em Execucao) vinculados a esta execucaoId)
    #lote = [{'filaId': 'filaId', 'status': 'status', 'parametroSaida': 'parametroSaida','mensagem': 'mensagem'}]"""
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'lote':lote,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada)
    return response.text

def filaAtualizarSucesso(execucaoId, filaId, saida, mensagem='Fila atualizada com sucesso'):
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'filaId':filaId,
        'statusId':2, #(0=aguardando, 1=em execucao, 2=encerrado com sucesso, 3=encerrado com erro)
        'Mensagem':mensagem,
        'parametroSaida': saida,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada)
    return response.text

def filaAtualizarProx(execucaoId, filaId, saida):
    """#elimina a necessidade de executar a chamada filaProximo, 
    #esta função atualiza o item e já retorna o proximo se existir"""
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'filaId':filaId,
        'statusId':2, #(0=aguardando, 1=em execucao, 2=encerrado com sucesso, 3=encerrado com erro)
        'Mensagem':'Fila atualizada com sucesso',
        'parametroSaida': saida,
        'proximo':'1',
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada)
    return response.text

def filaAtualizarFalha(execucaoId, filaId, mensagem, saida):
    entrada = {'token': token,
        'execucaoId':execucaoId,
        'filaId':filaId,
        'statusId':3, #(0=aguardando, 1=em execucao, 2=encerrado com sucesso, 3=encerrado com erro)
        'Mensagem':mensagem,
        'parametroSaida': saida,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }

    if usarProxy: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/atualizar", data=entrada)
    return response.text

def filaConsultar(execucaoId, criterio, ordenadoPor, limite=10, workflow=workflow_unico, tarefa=tarefa_unica):
    """Retorno:
    {"Autorizado": true,
    "Fila": [
        {
        "DataInclusao": "Fri, 01 Sep 2023 11:03:42 GMT",
        "DataInicioExecucao": "Mon, 29 Jan 2024 16:45:46 GMT",
        "DataUltimoStatus": "Mon, 29 Jan 2024 16:45:46 GMT",
        "ExecucaoId": "9c2c8d24-2cbd-4fbe-9ab6-d330166bfd47",
        "FilaId": "409ed1a7-eaf7-4dda-b46e-5c2f7b019b5a",
        "Mensagem": "Acionamento manual pelo site",
        "ParametrosEntrada": "{\"Email\": \"christian.marcondes@automate.com.br\", \"Nome\": \"Christian\"}",
        "ParametrosSaida": null,
        "Realocado": 0,
        "Referencia": "Execucao Manual",
        "StatusAlias": "EmExecucao",
        "StatusId": "1",
        "TarefaId": "2",
        "UsuarioId": ""
        }
    ],
    "Mensagem": ""}
    #Exemplos de criterios :
        #criterio = [{'Campo':'StatusId', 'Valor':'>0'}]
        #criterio = [{'Campo':'StatusId', 'Valor':'<2'},
        #            {'Campo':'Realocado', 'Valor':'=0'},
        #            {'Campo':'Referencia', 'Valor':'="cadastro Lote 01"'}]
        #criterio = [{'Campo':'Referencia', 'Valor':'like "%cadastro%"'}]
        #criterio = [{'Campo':'DataInclusao', 'Valor':'< "2023/06/26"'}]
        #criterio = json.dumps(criterio) #não esqueça de converter em json 
    # utilize qualquer campo de retorno acima como parametro Campo
    # em Valor utilize um sinal de comparação ('>', '<', '=', '<>' ou like ) e o valor a ser comparado
    """
    entrada={'token': token,
        'execucaoId': execucaoId,
        'workflow': workflow,
        'tarefa': tarefa,
        'criterios': criterio,
        'orderBy': ordenadoPor,
        'limite':limite,
        'funcao':inspect.stack()[0][3],
        'linhaComando':inspect.currentframe().f_back.f_lineno
    }
    if usarProxy: response = requests.request("POST", f"{SRShost}fila/consultar", data=entrada, proxies=proxy(), verify=False)
    else: response = requests.request("POST", f"{SRShost}fila/consultar", data=entrada)
    return response.text
