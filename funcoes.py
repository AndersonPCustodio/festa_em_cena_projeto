import pandas as pd
import re

def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(caminho_csv, sep=',', encoding='utf-8', dtype=str)
        print("=== SPRINT 1: INGESTÃO DE DADOS ===")
        print(f"Total de linhas lidas no arquivo original: {len(df)}")
        print("\nExemplo de 3 registros iniciais:")
        print(df.head(3))
        print("=" * 40 + "\n")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return pd.DataFrame()

def padronizar_strings(df: pd.DataFrame) -> tuple:
    df_limpo = df.copy()
    
    categorias_vazias_preenchidas = 0
    categorias_nao_vazias_alteradas = 0

    def limpar_categoria(valor):
        nonlocal categorias_vazias_preenchidas, categorias_nao_vazias_alteradas
        
        if pd.isna(valor) or str(valor).strip() == "":
            categorias_vazias_preenchidas += 1
            return "sem categoria"
            
        texto_original = str(valor)
        texto_processado = texto_original.strip().lower()
        texto_processado = re.sub(r'[^\w\s]', '', texto_processado)
        
        if texto_processado.strip() == "":
            categorias_vazias_preenchidas += 1
            return "sem categoria"
            
        if texto_processado != texto_original:
            categorias_nao_vazias_alteradas += 1
            
        return texto_processado

    def ajustar_canal(canal):
        if pd.isna(canal):
            return "Não Identificado"
        canal_str = str(canal).strip().lower()
        if 'web' in canal_str:
            return 'Web'
        elif 'loja' in canal_str or 'física' in canal_str or 'fisica' in canal_str:
            return 'Loja física'
        elif 'mercado' in canal_str:
            return 'Mercado'
        return str(canal).strip()

    if 'categoria' in df_limpo.columns:
        df_limpo['categoria'] = df_limpo['categoria'].apply(limpar_categoria)
        
    if 'canal_venda' in df_limpo.columns:
        df_limpo['canal_venda'] = df_limpo['canal_venda'].apply(ajustar_canal)

    print("=== SPRINT 2: TRANSFORMAÇÃO DE STRINGS ===")
    print(f"Categorias vazias preenchidas como 'sem categoria': {categorias_vazias_preenchidas}")
    print(f"Categorias modificadas/limpas por Regex: {categorias_nao_vazias_alteradas}")
    print("=" * 40 + "\n")

    return df_limpo, categorias_vazias_preenchidas, categorias_nao_vazias_alteradas

def validar_dados_numericos(df: pd.DataFrame) -> tuple:
    df_validado = df.copy()
    
    problemas_quantidade = 0
    problemas_preco = 0
    
    linhas_afetadas = set()
    
    for idx, linha in df_validado.iterrows():
        problema_na_linha = False
        
        qtd_original = linha.get('quantidade')
        try:
            qtd_num = int(float(qtd_original))
            if qtd_num <= 0:
                problemas_quantidade += 1
                problema_na_linha = True
        except (ValueError, TypeError):
            problemas_quantidade += 1
            problema_na_linha = True
            
        preco_original = linha.get('preco_unitario')
        if pd.isna(preco_original) or str(preco_original).strip() == "":
            problemas_preco += 1
            problema_na_linha = True
        else:
            try:
                preco_num = float(preco_original)
                if preco_num < 0:
                    problemas_preco += 1
                    problema_na_linha = True
            except (ValueError, TypeError):
                problemas_preco += 1
                problema_na_linha = True
                
        if problema_na_linha:
            linhas_afetadas.add(idx)
            
    total_pedidos_afetados = len(linhas_afetadas)
    
    print("=== SPRINT 3: VALIDAÇÃO DE NÚMEROS E NULOS ===")
    print(f"Pedidos com problemas na Quantidade: {problemas_quantidade}")
    print(f"Pedidos com problemas no Preço Unitário: {problemas_preco}")
    print(f"Total absoluto de pedidos afetados (sem sobreposição): {total_pedidos_afetados}")
    print("=" * 46 + "\n")
    
    return df_validado, problemas_quantidade, problemas_preco, total_pedidos_afetados

from datetime import datetime

def investigar_regra_negocio(df: pd.DataFrame) -> tuple:
    df_analise = df.copy()
    
    filtro_sem_entrega = pd.isna(df_analise['data_entrega']) | (df_analise['data_entrega'].astype(str).str.strip() == "")
    df_sem_entrega = df_analise[filtro_sem_entrega]
    
    df_sem_entrega_cancelados = df_sem_entrega[df_sem_entrega['status_pedido'].astype(str).str.strip().str.lower() == 'cancelado']
    cont_sem_entrega_cancelados = len(df_sem_entrega_cancelados)
    
    df_sem_entrega_outros = df_sem_entrega[df_sem_entrega['status_pedido'].astype(str).str.strip().str.lower() != 'cancelado']
    cont_sem_entrega_outros = len(df_sem_entrega_outros)
    
    hipotese_verdadeira = (cont_sem_entrega_outros == 0)
    
    exemplos_contraexemplo = df_sem_entrega_outros.head(3)[['pedido_id', 'status_pedido', 'data_entrega']].to_dict(orient='records')
    
    print("=== SPRINT 4 (PARTE 1): LÓGICA DE REGRA DE NEGÓCIO ===")
    print(f"Pedidos sem entrega E Cancelados: {cont_sem_entrega_cancelados}")
    print(f"Pedidos sem entrega COM OUTROS STATUS: {cont_sem_entrega_outros}")
    print(f"A hipótese de que toda entrega vazia é um pedido cancelado é: {hipotese_verdadeira}")
    
    if exemplos_contraexemplo:
        print("\nExemplos de contraexemplos encontrados na base:")
        for ex in exemplos_contraexemplo:
            print(f" -> ID Pedido: {ex['pedido_id']} | Status: {ex['status_pedido']} | Data Entrega: {ex['data_entrega']}")
    print("=" * 54 + "\n")
    
    return cont_sem_entrega_cancelados, cont_sem_entrega_outros, hipotese_verdadeira

def formatar_temporal(df: pd.DataFrame) -> tuple:
    df_temporal = df.copy()
    datas_invalidas_ou_vazias = 0
    
    anos, meses, dias, horas, datas_br = [], [], [], [], []
    
    for idx, linha in df_temporal.iterrows():
        data_orig = linha.get('data_venda')
        
        if pd.isna(data_orig) or str(data_orig).strip() == "":
            datas_invalidas_ou_vazias += 1
            anos.append(None); meses.append(None); dias.append(None); horas.append(None); datas_br.append("Data Inválida")
            continue
            
        try:
            data_limpa = str(data_orig).split('.')[0].strip()
            dt_objeto = datetime.strptime(data_limpa, "%Y-%m-%d %H:%M:%S")
            
            anos.append(dt_objeto.year)
            meses.append(dt_objeto.month)
            dias.append(dt_objeto.day)
            horas.append(dt_objeto.hour)
            datas_br.append(dt_objeto.strftime("%d/%m/%Y"))
            
        except Exception:
            datas_invalidas_ou_vazias += 1
            anos.append(None); meses.append(None); dias.append(None); horas.append(None); datas_br.append("Data Inválida")
            
    df_temporal['venda_ano'] = anos
    df_temporal['venda_mes'] = meses
    df_temporal['venda_dia'] = dias
    df_temporal['venda_hora'] = horas
    df_temporal['venda_data_br'] = datas_br
    
    print("=== SPRINT 4 (PARTE 2): FORMATTAÇÃO TEMPORAL ===")
    print(f"Total de datas de venda inválidas ou vazias puladas/marcadas: {datas_invalidas_ou_vazias}")
    print("=" * 48 + "\n")
    
    return df_temporal, datas_invalidas_ou_vazias

