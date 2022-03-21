import csv
import requests
#import ipdb
from bs4 import BeautifulSoup as BS

#O usuário deve atualizar o ano, abaixo, para a criação da nova planilha.
ANO = '2022'

#O usuário deve modificar a planilha de referência abaixo CASO DESEJE buscar as relações entre Conjuntos Elétricos e Municípios de todo o Brasil. Mudar para "./files/municipiosBR.csv"
PATH_MUNICIPIOS_CSV = '.\municipiosRJ.csv'


#Não editar o código abaixo
APP_HOST = "https://www2.aneel.gov.br/aplicacoes_liferay/srd/indqual/dspConjunto.cfm?ano=ANO&estado=SIGLA_ESTADO&municipio=COD_MUNICIPIO"
OUTPUT_CSV = f'.\output_conjuntos_eletricosRJ{ANO}.csv'
# municipio.csv "COD_ESTADO","SIGLA_ESTADO","COD_MUNICIPIO","MUNICIPIO"


csv_file = csv.reader(
    open(PATH_MUNICIPIOS_CSV, mode='r', encoding='utf-8'), delimiter=',')
output = csv.writer(
    open(OUTPUT_CSV, mode='w', encoding='utf-8', newline=""), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
output.writerow(
    ['ANO', 'COD_ESTADO', 'SIGLA_ESTADO', 'COD_MUNICIPIO',
     'NOME_MUNICIPIO', 'COD_CONJUNTO_ELETRICO', 'CONJUNTO_ELETRICO']
)

for row in csv_file:
    response = requests.post(
        APP_HOST.replace('ANO', ANO)\
        .replace('SIGLA_ESTADO', row[1])\
        .replace('COD_MUNICIPIO', row[2])
    )
    soup_doc = BS(response.text, 'html.parser')
    for conjunto_e in soup_doc.find_all('option')[1:]:
        output.writerow(
            [
                ANO,
                row[0],
                row[1],
                row[2],
                row[3],
                conjunto_e.attrs['value'],
                conjunto_e.text
            ]
        )
