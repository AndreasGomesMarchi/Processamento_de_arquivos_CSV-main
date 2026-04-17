from multiprocessing import Pool
import os
from file_handler import ler_csv

def testeDefLegal():
    print("Teste para ver se o main.py ver essa pasta")

def processar_e_somar(caminho):
    """Lê o arquivo e já devolve os valores somados por município."""
    dados = ler_csv(caminho)
    somas_por_municipio = {}

    for linha in dados:
        mun = linha.get('municipio_oj')
        if not mun: continue

        if mun not in somas_por_municipio:

            somas_por_municipio[mun] = {
                'julgados_2026': 0.0, 'casos_novos_2026': 0.0, 
                'dessobrestados_2026': 0.0, 'suspensos_2026': 0.0,
                'julgm2_a': 0.0, 'distm2_a': 0.0, 'suspm2_a': 0.0,
                'julgm2_ant': 0.0, 'distm2_ant': 0.0, 'suspm2_ant': 0.0, 'desom2_ant': 0.0,
                'julgm4_a': 0.0, 'distm4_a': 0.0, 'suspm4_a': 0.0,
                'julgm4_b': 0.0, 'distm4_b': 0.0, 'suspm4_b': 0.0
            }

        for campo in somas_por_municipio[mun]:
            try:
                valor = linha.get(campo, 0)
                somas_por_municipio[mun][campo] += float(valor if valor and str(valor).strip() != 'NA' else 0)
            except ValueError:
                pass
                
    return somas_por_municipio

def concatenar_paralelo(pasta_entrada):
    """Lê todos os CSVs da pasta em paralelo e retorna uma lista única."""
    arquivos = [os.path.join(pasta_entrada, f) for f in os.listdir(pasta_entrada) if f.endswith(".csv")]
    
    with Pool() as p:
        resultados = p.map(ler_csv, arquivos)
    
    dados_unificados = [linha for sublista in resultados for linha in sublista]
    return dados_unificados

def gerar_resumo_paralelo(pasta_entrada):
    arquivos = [os.path.join(pasta_entrada, f) for f in os.listdir(pasta_entrada) if f.endswith(".csv")]

    with Pool() as p:
        resultados_parciais = p.map(processar_e_somar, arquivos)

    consolidado = {}
    for parcial in resultados_parciais:
        for mun, valores in parcial.items():
            if mun not in consolidado:
                consolidado[mun] = valores
            else:
                for campo in valores:
                    consolidado[mun][campo] += valores[campo]

    return consolidado

def filtrar_chunk(args):
    """Função auxiliar para filtrar um pedaço (chunk) dos dados."""
    dados_chunk, municipio = args
    municipio = municipio.upper()
    return [d for d in dados_chunk if d.get('municipio_oj', '').upper() == municipio]

def filtrar_por_municipio_paralelo(dados, municipio):
    """Divide a lista de dados e filtra em paralelo."""
    num_processos = os.cpu_count()
    tamanho_chunk = len(dados) // num_processos
    chunks = [(dados[i:i + tamanho_chunk], municipio) for i in range(0, len(dados), tamanho_chunk)]
    
    with Pool(num_processos) as p:
        resultados = p.map(filtrar_chunk, chunks)
    
    return [item for sublist in resultados for item in sublist]
