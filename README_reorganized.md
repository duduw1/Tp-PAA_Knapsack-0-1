# TP PAA — Knapsack 0/1 (reorganizado)

Este arquivo substitui temporariamente o README para refletir a reorganização do projeto.

Estrutura do repositório (organizada)
- `src/` — implementações do problema (algoritmos)
- `scripts/` — scripts auxiliares e de benchmark
- `data/` — inputs de exemplo (JSON) e dados gerados
- `figs/` — figuras e gráficos (gerados pelos scripts)
- `report/` — versão principal do relatório LaTeX (`knapsack_report.tex`)

Comandos úteis

```powershell
# Executar benchmark (gera/usa data/input_32.json)
python .\scripts\knapsack_benchmark.py --input data\input_32.json --output data\results.csv --timeout 60

# Executar helper para implementação 4
python .\scripts\run4.py data\input_32.json

# Gerar gráficos
python .\scripts\plot_results.py
```

Observações
- Preferi criar este arquivo `README_reorganized.md` em vez de sobrescrever o README original automaticamente. Se quiser que eu substitua o README principal, posso fazê-lo agora.
