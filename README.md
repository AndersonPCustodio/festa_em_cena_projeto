# 🎃 Projeto Festa em Cena - Análise de Vendas de Halloween

Este projeto foi desenvolvido como **Mini-Projeto Avaliativo para o Módulo 1 (Semana 07) do curso de Machine Learning e Visão Computacional (Turma 05)** pela SCTEC. O objetivo é realizar a ingestão, limpeza, tratamento e exploração inicial de dados da rede de lojas fictícia Festa em Cena, aplicando boas práticas de programação modular e estruturada em Python com a biblioteca Pandas.

## 📝 Descrição do Projeto e Significado dos Dados
Uma linha nesta base representa **um pedido individual de um único produto**, o qual pode conter uma ou mais unidades adquiridas. Abaixo estão detalhadas quatro colunas principais do conjunto de dados:
* **pedido_id:** Identificador numérico exclusivo de controle de cada transação.
* **data_venda:** Timestamp correspondente ao momento exato em que a venda foi registrada no sistema.
* **canal_venda:** Canal de aquisição utilizado pelo comprador (Mercado, Loja física ou Web).
* **categoria:** Classificação geral do item comercializado (fantasias, acessórios, etc.).

### 🧠 Reflexão Teórica: Qualidade de Dados e Machine Learning
Antes de submeter qualquer conjunto de dados a modelos preditivos ou estatísticos em Machine Learning, a etapa de higienização de dados é indispensável. Informações omissas, strings inconsistentes, ruídos operacionais e falhas de digitação enviesam as métricas de performance. 
Entretanto, **é fundamental ressaltar que a limpeza isolada dos dados não é uma garantia absoluta contra problemas de overfitting ou underfitting**. Mitigar esses fenômenos exige uma abordagem holística que abrange a garantia de representatividade estatística da amostra, a seleção de algoritmos adequados à complexidade do problema e uma estratégia rigorosa de validação cruzada.

---

## 🛠️ Regras de Tratamento e Negócio Adotadas
* **Textos:** Strings na coluna `categoria` passaram pela remoção de espaçamentos inúteis (`.strip()`), conversão para letras minúsculas (`.lower()`) e filtragem por Expressões Regulares (`re.sub`) para eliminar pontuações indevidas. Campos completamente nulos ou vazios pós-tratamento receberam a classificação `"sem categoria"`. A coluna `canal_venda` foi padronizada sob uma regra condicional mapeando variações textuais para as categorias exatas exigidas: `Mercado`, `Loja física` e `Web`.
* **Valores Numéricos:** Verificou-se que `quantidade` deve consistir estritamente em valores inteiros estritamente maiores que zero. Para a coluna `preco_unitario`, os registros válidos devem estar preenchidos e não podem conter números negativos. Linhas inconsistentes foram computadas e reportadas de forma única, evitando sobreposição de erros em um mesmo pedido.
* **Datas:** strings de datas foram convertidas utilizando o método nativo `datetime.strptime()`. Registros corrompidos foram mantidos com marcações nulas (`None`) no pipeline temporal para não interromper a execução do fluxo e nem distorcer as análises históricas com a substituição arbitrária pela data presente.

---

## 🚀 Guia de Execução e Configuração do Ambiente

### Pré-requisitos
Certifique-se de possuir o Python 3.8+ instalado em sua máquina juntamente com a biblioteca Pandas.

```bash
pip install pandas
```

### Como Executar
1. Clone este repositório ou baixe os arquivos em uma mesma pasta de trabalho.
2. Certifique-se de que a base `halloween_vendas.csv` está localizada na raiz do diretório.
3. Abra o terminal na pasta do projeto e execute o pipeline central através do comando:
```bash
python main.py
```
