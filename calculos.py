def aplicar_formulas(s):
    """Calcula as metas baseadas nos somatórios fornecidos."""
   
    denominador_m1 = (s['casos_novos_2026'] + s['dessobrestados_2026'] - s['suspensos_2026'])
    meta1 = (s['julgados_2026'] / denominador_m1 * 100) if denominador_m1 != 0 else 0
    
    denominador_m2a = (s['distm2_a'] - s['suspm2_a'])
    meta2a = (s['julgm2_a'] / denominador_m2a * (1000/7)) if denominador_m2a != 0 else 0


    denominador_m2ant = (s['distm2_ant'] - s['suspm2_ant'] - s['desom2_ant'])
    meta2ant = (s['julgm2_ant'] / denominador_m2ant * 100) if denominador_m2ant != 0 else 0

    denominador_m4a = (s['distm4_a'] - s['suspm4_a'])
    meta4a = (s['julgm4_a'] / denominador_m4a * 100) if denominador_m4a != 0 else 0

    denominador_m4b = ( s['distm4_b'] - s['suspm4_b'])
    meta4b = (s['julgm4_b'] / denominador_m4b * 100) if denominador_m4b != 0 else 0

    return {
        'Meta1': meta1,
        'Meta2A': meta2a,
        'Meta2Ant': meta2ant,
        'Meta4A':   meta4a,
        'Meta4B':   meta4b,
    }

def gerar_ranking_tribunais(dados, top_n=10):
    """Agrupa os dados por tribunal, Meta1, Meta2A, Meta2Ant, Meta4A e Meta4B e retorna os top n ordenados por Meta1 decrescente"""
    agrupado = {}

    campos_numericos = [
        'julgados_2026', 'casos_novos_2026', 'dessobrestados_2026', 'suspensos_2026',
        'distm2_a',   'julgm2_a',   'suspm2_a',
        'distm2_ant', 'julgm2_ant', 'suspm2_ant', 'desom2_ant',
        'distm4_a',   'julgm4_a',   'suspm4_a',
        'distm4_b',   'julgm4_b',   'suspm4_b',
    ]

    for linha in dados:
        tribunal = linha.get('sigla_tribunal', '').strip()
        if not tribunal:
            continue

        if tribunal not in agrupado:
            agrupado[tribunal] = {k: 0.0 for k in campos_numericos}

        for campo in campos_numericos:
            try:
                valor = linha.get(campo, 0)
                agrupado[tribunal][campo] += float(
                    valor if valor and str(valor).strip() not in ('', 'NA') else 0
                )
            except (ValueError, TypeError):
                pass
    
    ranking = []

    for tribunal, valores in agrupado.items():
        metas = aplicar_formulas(valores)
        ranking.append({
            'sigla_tribunal': tribunal,
            'Meta1':          round(metas['Meta1'],    2),
            'Meta2A':         round(metas['Meta2A'],   2),
            'Meta2Ant':       round(metas['Meta2Ant'], 2),
            'Meta4A':         round(metas['Meta4A'],   2),
            'Meta4B':         round(metas['Meta4B'],   2),
        })

    ranking.sort(key=lambda x: (x['Meta1'], x['Meta2A']), reverse=True)  

    top = ranking[:top_n]

    for i, item in enumerate(top, 1):
        item['posicao'] = i

    return [
        {
            'posicao':        item['posicao'],
            'sigla_tribunal': item['sigla_tribunal'],
            'Meta1':          item['Meta1'],
            'Meta2A':         item['Meta2A'],
            'Meta2Ant':       item['Meta2Ant'],
            'Meta4A':         item['Meta4A'],
            'Meta4B':         item['Meta4B'],
        }
        for item in top
    ]

def gerar_top_10_tribunais(dados):
    return gerar_ranking_tribunais(dados, top_n=10)

def processar_resumo(dados, campo_agrupamento):
    """Agrupa os dados e garante que todos os campos das fórmulas sejam somados."""
    agrupado = {}
    
    # Todos os campos necessários para as 5 metas citadas no PDF / Alterei para tudo ficar dentro duma variavel pq o codigo estava gigantescco ali kkkkkkk
    campos_necessarios = [
        'julgados_2026', 'casos_novos_2026', 'dessobrestados_2026', 'suspensos_2026',
        'julgm2_a', 'distm2_a', 'suspm2_a',
        'julgm2_ant', 'distm2_ant', 'suspm2_ant', 'desom2_ant',
        'julgm4_a', 'distm4_a', 'suspm4_a',
        'julgm4_b', 'distm4_b', 'suspm4_b'
    ]

    for linha in dados:
        chave = linha.get(campo_agrupamento)
        if not chave: continue
        
        if chave not in agrupado:
            agrupado[chave] = {k: 0.0 for k in campos_necessarios}
        
        for campo in campos_necessarios:
            try:
                valor = linha.get(campo, 0)
                agrupado[chave][campo] += float(valor if valor and str(valor).strip() != 'NA' else 0)
            except: pass

    resultado = []
    for chave, valores in agrupado.items():
        metas = aplicar_formulas(valores)
        item = {campo_agrupamento: chave}
        item.update({k: round(v, 2) for k, v in metas.items()})
        resultado.append(item)
    
    return resultado

