# 📊 Relatório Técnico de Exploração de Dados – Festa em Cena

Este relatório apresenta o diagnóstico de qualidade de dados e a análise exploratória inicial da base de registros da Festa em Cena, abrangendo as operações de agosto a novembro de 2024 e 2025. O objetivo central é munir a gestão com evidências numéricas que subsidiem decisões estratégicas e corrijam falhas operacionais antes de qualquer iniciativa de modelagem preditiva.

## 1. Diagnóstico de Qualidade e Integridade dos Dados
O processo de auditoria identificou anomalias severas em múltiplas dimensões do conjunto de dados original:
* **Inconsistências Textuais:** Foram localizadas 18 ocorrências de categorias inteiramente omitidas ou nulas, além de 1.482 registros contendo ruídos, pontuações indevidas ou formatações heterogêneas na coluna de categorias. Todas foram limpas via expressões regulares ou mapeadas como "sem categoria".
* **Falhas de Consistência Numérica:** Um total de 19 pedidos exclusivos apresentou não conformidades financeiras ou operacionais. Especificamente, detectou-se 7 registros com quantidades de itens inválidas (valores nulos, zerados ou negativos) e 12 transações com preços unitários ausentes ou corrompidos.
* **Vulnerabilidades Temporais:** O pipeline isolou 4 registros com a data de venda corrompida ou ausente, os quais foram desconsiderados nos agrupamentos cronológicos para evitar distorções estatísticas.

## 2. Validação de Regra de Negócio (Hipótese de Entrega)
A direção postulava a hipótese de que a ausência de uma data de entrega preenchida estaria estritamente associada ao cancelamento do pedido. **A análise exploratória refutou categoricamente esta premissa.** 
Embora 109 pedidos sem data de entrega correspondam de fato a transações com status "Cancelado", foram identificados **34 contraexemplos críticos** (como os pedidos de ID 1170, 990 e 740). Nestes casos, o status consta como "Concluído", mas o campo de entrega permanece nulo. Esta desconexão expõe uma falha sistêmica de fechamento de dados ou gargalos graves na roteirização logística.

## 3. Descobertas Estratégicas e Limitações
A consolidação volumétrica revelou que o canal Web lidera de forma isolada a preferência dos consumidores, seguido pela Loja Física e, por último, o canal Mercado. Cronologicamente, o volume de pedidos apresenta um comportamento de forte sazonalidade anual, registrando picos expressivos concentrados no mês de outubro, alinhando-se diretamente ao período de celebração do Halloween, com quedas acentuadas nos meses adjacentes.

**Limitação Teórica:** Salienta-se que os volumes computados traduzem ordens de pedidos registradas no banco de dados e não faturamento líquido ou receitas efetivamente auferidas, dado o alto índice de registros corrompidos e pedidos marcados como concluídos sem evidência física de entrega.
