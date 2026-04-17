import file_handler
import time
import calculos
import CSVParalelo as Paralelo

PASTA = "Base de Dados"
OUTPUT_SERIAL = "output/unificado_serial.csv"
OUTPUT_PARALELO = "output/unificado_paralelo.csv"

def menu():
    print("\n1 - Concatenar CSV (Serial)")
    print("2 - Concatenar CSV (Paralelo)")
    print("3 - Filtrar por município")
    print("4 - Listar municípios disponíveis")
    print("5 - Gerar Resumo por Município (Serial)")
    print("6 - Gerar Resumo por Município (Paralelo)")
    print("7 - Exibir Top 10 Tribunais")
    print("0 - Sair")   


def main():
    while True:
        menu()
        op = input("Escolha: ")

        if op == "1":
            inicio = time.time()
            file_handler.concatenar_csvs(PASTA, OUTPUT_SERIAL)
            print("Tempo:", time.time() - inicio)
            

        elif op == "2":
            inicio = time.time()
            dados = Paralelo.concatenar_paralelo(PASTA)
            file_handler.escrever_csv(OUTPUT_PARALELO, dados, dados[0].keys())
            print("Tempo:", time.time() - inicio)

        elif op == "3":
            municipio = input("Digite o município: ").upper()
            dados = file_handler.ler_csv(OUTPUT_SERIAL) # Base completa
            
            # Exemplo de escolha de versão para cumprir o requisito 
            modo = input("1-Serial / 2-Paralelo: ")
            if modo == "1":
                filtrado = file_handler.filtrar_por_municipio(dados, municipio)
            else:
                filtrado = Paralelo.filtrar_por_municipio_paralelo(dados, municipio)

            # Salvar como CSV conforme o exemplo "MACAPA.csv" [cite: 23]
            file_handler.escrever_csv(f"output/{municipio}.csv", filtrado, dados[0].keys())
            print(f"Arquivo CSV para {municipio} gerado com sucesso!")

        elif op == "4":
            tipo = input("Usar dados (1-Serial / 2-Paralelo): ")

            if tipo == "1":
                dados = file_handler.ler_csv(OUTPUT_SERIAL)
            else:
                dados = file_handler.ler_csv(OUTPUT_PARALELO)

            dados = file_handler.padronizar(dados)

            municipios = sorted(set(d['municipio_oj'] for d in dados))

            print("\nMunicípios disponíveis:")
            for m in municipios:
                print(m)
        
        elif op == "5":
            print("Gerando resumo por município (Serial)...")
            inicio = time.time()
            dados = file_handler.ler_csv(OUTPUT_SERIAL) 
            resumo = calculos.processar_resumo(dados, 'municipio_oj')
            file_handler.escrever_csv("output/resumo_municipios_serial.csv", resumo, resumo[0].keys())
            print(f"Concluído em: {time.time() - inicio:.4f}s")

        elif op == "6":
            print("Gerando resumo por município (Paralelo)...")
            inicio = time.time()
            resumo_dict = Paralelo.gerar_resumo_paralelo(PASTA)
            resumo_lista = list(resumo_dict.values())
            file_handler.escrever_csv("output/resumo_municipios_paralelo.csv", resumo_lista, resumo_lista[0].keys())
            print(f"Concluído em: {time.time() - inicio:.4f}s")

        elif op == "7":
            print("\n--- TOP 10 TRIBUNAIS (META 1) ---")
            
            tipo = input("Usar dados (1-Serial / 2-Paralelo): ")

            if tipo == "1":
                dados = file_handler.ler_csv(OUTPUT_SERIAL)
            else:
                dados = file_handler.ler_csv(OUTPUT_PARALELO)


            dados = file_handler.padronizar(dados)

            top10 = calculos.gerar_top_10_tribunais(dados)

            if not top10:
                print("Nenhum dado disponível.")
                continue
            

            print(f"\n{'Pos':<4} {'Tribunal':<12} {'Meta1':>8} {'Meta2A':>8} {'Meta2Ant':>10} {'Meta4A':>8} {'Meta4B':>8}")
            print("-" * 62)
            for trib in top10:
                print(
                    f"{trib['posicao']:<4} {trib['sigla_tribunal']:<12}"
                    f" {trib['Meta1']:>7.2f}%"
                    f" {trib['Meta2A']:>7.2f}%"
                    f" {trib['Meta2Ant']:>9.2f}%"
                    f" {trib['Meta4A']:>7.2f}%"
                    f" {trib['Meta4B']:>7.2f}%"
                )

            saida = "output/top10_tribunais.csv"
            file_handler.escrever_csv(saida, top10, top10[0].keys())
            print(f"\nArquivo salvo em: {saida}")
        
        elif op == "0":
            break


if __name__ == "__main__":
    main()