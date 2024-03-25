import requests
from datetime import date, timedelta

#pega datas de hoje e quinze dias atás
hojeData = date.today()
quinzeDiasAtrasData = hojeData - timedelta(days=15)

#formata de acordo com API do banco central
hojeStr = hojeData.strftime(r"%m-%d-%Y")
quinzeDiasAtrasStr = quinzeDiasAtrasData.strftime(r"%m-%d-%Y")


#faz GET no endpoint de cotação dos últimos 10 dias e salva em JSON
try:
    response = requests.get("https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial=%27{}%27&@dataFinalCotacao=%27{}%27&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda".format(quinzeDiasAtrasStr, hojeStr))
    response_json = response.json()

    #puxa os valores da resposta
    valores = response_json['value']

    #printa os valores de compra e venda, no fechamento de cada dia
    deltaData = float(11)
    print("\nCotação Dólar dos últimos 10 dias:\n")
    for valor in valores:
        print(str(hojeData - timedelta(days=deltaData)) + " | USD | " + "Compra: " + str(valor['cotacaoCompra']).replace('.',',') + " | " + "Venda: " + str(valor['cotacaoVenda']).replace('.',','))
        deltaData -= 1

except:
    print("Erro ao buscar cotações dos últimos 10 dias")


#faz GET no endpoint da cotação de hoje e salva em JSON
try:
    responseCotacaoHoje = requests.get(" https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaAberturaOuIntermediario(codigoMoeda=@codigoMoeda,dataCotacao=@dataCotacao)?@codigoMoeda='USD'&@dataCotacao='{}'&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao".format(hojeStr))
    responseCotacaoHoje_json = responseCotacaoHoje.json()

    #puxa os valores da resposta
    valorCotacaoHoje = responseCotacaoHoje_json['value']

    #printa a cotação de hoje junto com o horário
    print("\nCotação de Hoje:\n\n{} | USD | Compra: {} | Venda: {} \n".format(valorCotacaoHoje[0]['dataHoraCotacao'] ,str(valorCotacaoHoje[0]['cotacaoCompra']).replace('.',','),str(valorCotacaoHoje[0]['cotacaoVenda']).replace('.',',')))

except:
    print("Erro ao buscar cotação de hoje")




