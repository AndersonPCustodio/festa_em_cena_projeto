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

