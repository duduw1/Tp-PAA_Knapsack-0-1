# TP PAA — Knapsack 0/1

Este repositório contém implementações e experimentos para o problema "Knapsack 0/1" usados no trabalho de PAA.

Estrutura principal
- `1.py` — implementação recursiva (ingênua, exponencial)
- `2.py` — implementação top-down (memoização)
- `3.py` — heurística gulosa (valor/peso)
- `4.py` — programação dinâmica (bottom-up) com reconstrução dos itens escolhidos
- `knapsack_benchmark.py` — runner para carregar `1.py..4.py`, medir tempos e salvar resultados em CSV
- `run4.py` — helper para executar apenas a implementação em `4.py` com um arquivo JSON de entrada
- `input_5.json`, `input_10.json`, `input_20.json`, `input_32.json`, `input_32.json` — exemplos de entrada
- `input_large.json` — exemplo maior
- `knapsack_report.tex` — LaTeX do relatório (gerado automaticamente)

Como usar

1. Instale dependências (opcional)

   Se for usar scripts que dependem de `numpy` ou outras bibliotecas, crie um ambiente virtual e instale:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Rodar o runner de benchmark (gera/usa `input.json` e salva `results.csv`):

```powershell
Set-Location 'C:\Users\ThorG\Documents\2025.2\paa\tp'
python .\knapsack_benchmark.py --input input_32.json --output results.csv --timeout 60
```

3. Rodar apenas a implementação `4.py` (DP com reconstrução) usando `run4.py`:

```powershell
python .\run4.py input_32.json
```

4. Gerar entrada aleatória e rodar:

```powershell
python .\knapsack_benchmark.py --generate --n 50 --capacity 200 --input random.json
python .\knapsack_benchmark.py --input random.json --output results.csv
```

Observações
- `results.csv` está no `.gitignore` por padrão para evitar commitar medições locais — remova essa linha se desejar versionar os resultados.
- O `knapsack_report.tex` gerado resume os resultados e inclui instruções para compilação com pdflatex/Overleaf.

Contribuições
- Sinta-se livre para abrir issues/PRs no repositório remoto para melhorias, scripts de plotagem, ou para adicionar testes automatizados.
