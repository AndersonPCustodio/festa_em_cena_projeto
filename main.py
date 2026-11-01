from funcoes import (
    carregar_dados, 
    padronizar_strings, 
    validar_dados_numericos, 
    investigar_regra_negocio, 
    formatar_temporal,
    explorar_canais_e_periodos
)

def executar_pipeline():
    caminho_arquivo = "halloween_vendas.csv"
    
    df_vendas = carregar_dados(caminho_arquivo)
    
    if not df_vendas.empty:
        df_vendas_tratado, cat_vazias, cat_alteradas = padronizar_strings(df_vendas)
        
        df_vendas_validado, prob_qtd, prob_preco, total_afetados = validar_dados_numericos(df_vendas_tratado)
        
        cont_canc, cont_outros, hip_verdade = investigar_regra_negocio(df_vendas_validado)
        df_vendas_final, datas_inv = formatar_temporal(df_vendas_validado)
        
        explorar_canais_e_periodos(df_vendas_final)

if __name__ == "__main__":
    executar_pipeline()
