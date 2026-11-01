from funcoes import carregar_dados, padronizar_strings

def executar_pipeline():
    caminho_arquivo = "halloween_vendas.csv"
    
    df_vendas = carregar_dados(caminho_arquivo)
    
    if not df_vendas.empty:
        df_vendas_tratado, cat_vazias, cat_alteradas = padronizar_strings(df_vendas)

if __name__ == "__main__":
    executar_pipeline()
