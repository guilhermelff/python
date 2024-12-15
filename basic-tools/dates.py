import easygui
import pandas as pd
import locale
import json
from datetime import datetime, date, time
import sys
from unidecode import unidecode
import math


def valida_data_sap(data) -> str:

    if isinstance(data, str):
        if "/" in data:
            str_data_formatada = datetime.strptime(data, "%d/%m/%Y")
            str_data_formatada = data_formatada.strftime('%d.%m.%Y')
        print(f"{type(data_date)} {data_date}")

    elif isinstance(data_documento, datetime.datetime):
        if "/" in data_documento:
            data_date = data_documento.strftime('%d.%m.%Y')
        elif "." in data_documento:
            data_date = data_documento.strftime('%d.%m.%Y')

    else:
        print("data fora do padrão d m Y")


data_documento = r"01/02/2023"
df_dates = pd.read_excel("data\dates.xlsx", header=None)

for index, row in df_dates.iterrows():
    data_excel = row[0]
    print(data_excel)

print(type(data_documento))


