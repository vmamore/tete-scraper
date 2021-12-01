from bs4 import BeautifulSoup
import requests
import sqlite3
from sqlite3 import Error

sql_create_notas_fiscais_table = """ CREATE TABLE IF NOT EXISTS notas_fiscais (
                                    id integer PRIMARY KEY,
                                    url text NOT NULL,
                                    qr_code text NOT NULL,
                                    mercado_cnpj text NOT NULL,
                                    mercado_endereco text NOT NULL,
                                    mercado_nome text NOT NULL,
                                    creation_date text NOT NULL
                                ); """

sql_create_itens_table = """ CREATE TABLE IF NOT EXISTS itens (
                                    id integer PRIMARY KEY,
                                    titulo text NOT NULL,
                                    quantidade integer NOT NULL,
                                    unidade text NOT NULL,
                                    valor_unitario text NOT NULL,
                                    valor_total text NOT NULL,
                                    nota_fiscal_id integer NOT NULL,
                                    FOREIGN KEY (nota_fiscal_id) REFERENCES notas_fiscais (id)
                                ); """


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def initialize_db():
    conn = create_connection('C:\\Labs\\tete-scraper\\tete.db')
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_notas_fiscais_table)

        # create tasks table
        create_table(conn, sql_create_itens_table)
    else:
        print("Error! cannot create the database connection.")


class NotaFiscal:
    def __init__(self, url, qr_code, mercado_cnpj, mercado_endereco, mercado_nome):
        self.url = url
        self.qr_code = qr_code
        self.mercado_cnpj = mercado_cnpj
        self.mercado_endereco = mercado_endereco
        self.mercado_nome = mercado_nome


class Item:
    def __init__(self, item_dictionary):
        # print(item_dictionary)
        self.titulo = item_dictionary['txtTit']
        self.quantidade = item_dictionary['Rqtd']
        self.unidade = item_dictionary['RUN']
        self.valor_unitario = item_dictionary['RvlUnit']
        self.valor_total = item_dictionary['valor']


URL = 'http://www.dfe.ms.gov.br/nfce/qrcode/?p=50211104757459002643655110000560801400111991|2|1|1|6E14978CEEC9E77F4FA433C5199D865111067583'


if __name__ == '__main__':
    initialize_db()
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
        item = Item(item_dict)
        print(item)
# for titles in soup.find_all('span', 'txtTit'):
#     print(titles)

