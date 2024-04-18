import pandas as pd

def verifica_compensacao(path:str):
    
    df = pd.read_excel(path)
    
    for index, row in df.iterrows():
        
        tipo_compensacao = row["Tipo de compensação"]

        match tipo_compensacao:
            case "Adiantamento de cliente":
                print("Adiantamento de cliente")

            case "Estorno de nota fiscal ou nota de crédito":
                print("Estorno de nota fiscal ou nota de crédito")

            case "Conta de DNI":
                print("Conta de DNI")
            
            case "Adiantamento de cliente - Receita acessória":
                print("Adiantamento de cliente - Receita acessória")

            case "Adiantamento de cliente - Receita de Serviço de Transmissão de Dados":
                print("Adiantamento de cliente - Receita de Serviço de Transmissão de Dados")

            case "Adiantamento de cliente - Receita de Serviço de Internet":
                print("Adiantamento de cliente - Receita de Serviço de Internet")
            
            case "Adiantamento de cliente - Receita de Serviço de Instalação":
                print("Adiantamento de cliente - Receita de Serviço de Instalação")

            case "Adiantamento de cliente - Leilão":
                print("Adiantamento de cliente - Leilão")

            case "Adiantamento de cliente - Receitas Aeroportuárias de Passageiros":
                print("Adiantamento de cliente - Receitas Aeroportuárias de Passageiros")

            case "Adiantamento de cliente - Receita Aeroportuárias de Aeronaves":
                print("Adiantamento de cliente - Receita Aeroportuárias de Aeronaves")

            case "Adiantamento de cliente - Receita Aeroportuária por uso da Infraestrutura":
                print("Adiantamento de cliente - Receita Aeroportuária por uso da Infraestrutura")

            case "Adiantamento de cliente - Receita Aeroportuária de Cargas":
                print("Adiantamento de cliente - Receita Aeroportuária de Cargas")

            case "Adiantamento de cliente - Alugueis - Aeroportos":
                print("Adiantamento de cliente - Alugueis - Aeroportos")

            case "Adiantamento de cliente - Concessões Comerciais - Aeroportos":
                print("Adiantamento de cliente - Concessões Comerciais - Aeroportos")

            case "Adiantamento de cliente - Estacionamento - Aeroportos":
                print("Adiantamento de cliente - Estacionamento - Aeroportos")

            case "Adiantamento de cliente - Propaganda - Aeroportos":
                print("Adiantamento de cliente - Propaganda - Aeroportos")

            case "Adiantamento de cliente - Outras Receitas Comerciais Aeroportos":
                print("Adiantamento de cliente - Outras Receitas Comerciais Aeroportos")

            case "Adiantamento de cliente - Intercompany":
                print("Adiantamento de cliente - Intercompany")

            case "Adiantamento de cliente - Dbtrans Cupom":
                print("Adiantamento de cliente - Dbtrans Cupom")

            case "Adiantamento de cliente - AVI":
                print("Adiantamento de cliente - AVI")

            case "Adiantamento de cliente - Visa":
                print("Adiantamento de cliente - Visa")

            case "Adiantamento de cliente - Lançamento de caução":
                print("Adiantamento de cliente - Lançamento de caução")

            case "Adiantamento de cliente - Cargas especiais/excedentes":
                print("Adiantamento de cliente - Cargas especiais/excedentes")

            case "Adiantamento de cliente - Liberação de animais":
                print("Adiantamento de cliente - Liberação de animais")
            

        

path = r"data\teste-09042024-152239_-_P12-ContasReceber-H3_Compensacoes_Estorno_de_nota_fiscal_ou_nota_de_credito.xlsx"
verifica_compensacao(path)