from bs4 import BeautifulSoup
import requests
import re


class Item:
    def __init__(self, titulo, quantidade, unidade, valor_unitario, valor_total):
        self.titulo = titulo
        self.quantidade = quantidade
        self.unidade = unidade
        self.valor_unitario = valor_unitario
        self.valor_total = valor_total


URL = 'http://www.dfe.ms.gov.br/nfce/qrcode/?p=50211104757459002643655110000560801400111991|2|1|1|6E14978CEEC9E77F4FA433C5199D865111067583'


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    response = requests.get(URL)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    print(soup.prettify())
    print('------------------------ TABLE > TR > SPANS ------------------------')
    trs = soup.find_all('tr')
    items = []
    for tr in trs:
        print('------------------------ TR ------------------------')
        print(tr['id'])
        spans = tr.find_all('span')
        item_dict = {}
        print('------------------------ SPANS ------------------------')
        for span in spans:
            # print(span)
            class_name = span['class'][0].replace(" ", "")
            value = span.text.replace(" ", "").replace("\n", "")
            item_dict[class_name] = value
            items.append(item_dict)
        print(item_dict)
# for titles in soup.find_all('span', 'txtTit'):
#     print(titles)

