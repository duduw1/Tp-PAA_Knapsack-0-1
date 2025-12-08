# TP PAA — Knapsack 0/1

Este repositório contém implementações e experimentos para o problema "Knapsack 0/1" (Problema da Mochila) desenvolvidos para a disciplina de Projeto e Análise de Algoritmos (PAA).

## Estrutura do Projeto

### Implementações dos Algoritmos
- `1_brutalF.py`: Implementação ingênua (força bruta recursiva).
- `2_pd.py`: Implementação com Programação Dinâmica (bottom-up, espaço otimizado).
- `3_greed.py`: Heurística gulosa (baseada na razão valor/peso).
- `4_pd_com_itens.py`: Programação Dinâmica completa que reconstrói e retorna os itens escolhidos.

### Scripts Auxiliares e Relatório
- `knapsack_benchmark.py`: Script principal para rodar benchmarks comparativos entre as implementações.
- `run4.py`: Utilitário para rodar especificamente o algoritmo 4 com um arquivo JSON de entrada.
- `scripts/random_tests.py`: Script para gerar casos de teste aleatórios e validar as implementações.
- `knapsack_report.tex`: Código fonte LaTeX do relatório final.

## Como Usar

### 1. Pré-requisitos
Certifique-se de ter o Python instalado. É recomendado usar um ambiente virtual se for instalar dependências externas (como `matplotlib` para gráficos, se necessário).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# source .venv/bin/activate    # Linux/Mac
pip install -r requirements.txt # Se houver arquivo de requisitos
```

### 2. Rodar Benchmark
Para comparar os algoritmos e salvar os resultados em CSV:

```powershell
python knapsack_benchmark.py --input input_32.json --output results.csv --timeout 60
```

### 3. Testar Implementação Otimizada (Algoritmo 4)
Para rodar apenas a solução ótima com reconstrução de itens:

```powershell
python run4.py input_32.json
```

### 4. Rodar Testes Aleatórios
Para gerar instâncias aleatórias e verificar a corretude e desempenho:

```powershell
python scripts/random_tests.py
```

## Relatório
O arquivo `knapsack_report.tex` contém a análise detalhada dos algoritmos, complexidade e resultados experimentais. Ele pode ser compilado usando qualquer distribuição LaTeX ou importado diretamente no Overleaf.

## Autores
Trabalho desenvolvido para a disciplina de PAA.
