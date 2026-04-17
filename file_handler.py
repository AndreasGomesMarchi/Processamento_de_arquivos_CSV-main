import csv
import os

# Ler um CSV
def ler_csv(caminho):
    with open(caminho, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


# Escrever CSV
def escrever_csv(caminho, dados, cabecalho):
    with open(caminho, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(dados)


# Concatenar vários CSVs
def concatenar_csvs(pasta_entrada, arquivo_saida):
    todos_dados = []
    cabecalho = None

    for arquivo in os.listdir(pasta_entrada):
        if arquivo.endswith(".csv"):
            caminho = os.path.join(pasta_entrada, arquivo)
            dados = ler_csv(caminho)

            if not cabecalho:
                cabecalho = dados[0].keys()

            todos_dados.extend(dados)

    escrever_csv(arquivo_saida, todos_dados, cabecalho)
    print("CSV unificado criado!")


# Filtrar por município
def filtrar_por_municipio(dados, municipio):
    municipio = municipio.upper()
    filtrado = [d for d in dados if d['municipio_oj'].upper() == municipio]
    return filtrado


# Padronizar dados (exemplo simples)
def padronizar(dados):
    for d in dados:
        d['municipio_oj'] = d['municipio_oj'].upper().strip()
    return dados