"""  
Programação Dinâmica para o problema da mochila 0/1 com reconstrução de itens.

Fornece duas funções:
- `knapsack(W, val, wt)` -> retorna o valor total máximo (int) (mantém compatibilidade)
- `knapsack_with_items(W, val, wt)` -> retorna (valor_total, indices_escolhidos)

Quando executado como script, demonstra o algoritmo e imprime quais itens foram
escolhidos (por índice) e o valor total.
"""

# Variável global para contar operações (células preenchidas)
OPS = 0

def knapsack_with_items(W, val, wt):
	"""
	PD Bottom-up para mochila 0/1 que também reconstrói os itens escolhidos.

	Retorna uma tupla (max_value, chosen_indices) onde chosen_indices é uma lista
	de índices de itens (base 0) que foram selecionados para alcançar o max_value. 
    A reconstrução prefere itens de índice mais alto primeiro quando ocorrem empates 
    devido à ordem de backtracking.
	"""
	global OPS
	OPS = 0
	
	n = len(val)
	# dp[i][w] = valor máximo usando os primeiros i itens (itens 0..i-1) com capacidade w
	dp = [[0] * (W + 1) for _ in range(n + 1)]

	for i in range(1, n + 1):
		vi = val[i - 1]
		wi = wt[i - 1]
		for w in range(0, W + 1):
			OPS += 1
			if wi <= w:
				# escolher ou não escolher
				pick = vi + dp[i - 1][w - wi]
				not_pick = dp[i - 1][w]
				dp[i][w] = max(pick, not_pick)
			else:
				# não pode escolher pois excede a capacidade atual
				dp[i][w] = dp[i - 1][w]

	# Reconstruir itens escolhidos (Backtracking na tabela DP)
	chosen = []
	w = W
	for i in range(n, 0, -1):
		OPS += 1 # operação de backtracking
		if dp[i][w] != dp[i - 1][w]:
			# o item i-1 foi pego
			chosen.append(i - 1)
			w -= wt[i - 1]
			if w <= 0:
				break

	chosen.reverse()
	return dp[n][W], chosen


def knapsack(W, val, wt):
	"""Wrapper de compatibilidade que retorna apenas o valor máximo (int)."""
	max_val, _ = knapsack_with_items(W, val, wt)
	return max_val


if __name__ == '__main__':
	# Exemplo de demonstração
	val = [1, 2, 3]
	wt = [4, 5, 1]
	W = 4

	total, items = knapsack_with_items(W, val, wt)
	print(f"Valor máximo: {total}")
	print(f"Índices dos itens escolhidos: {items}")
	print(f"Operações: {OPS}")