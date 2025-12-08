# [Aproximação] Abordagem Gulosa (razão valor/peso) - Tempo O(n log n)

# Variável global para contar operações (comparações/acessos principais)
OPS = 0

def knapsack(W, val, wt):
    """
    Aproximação gulosa para o problema da mochila 0/1: ordena os itens pela razão valor/peso
    e seleciona enquanto a capacidade permitir. Isso não é ótimo no caso geral,
    mas é rápido e útil para instâncias grandes.

    Retorna o valor total dos itens escolhidos.
    """
    global OPS
    OPS = 0
    
    n = len(val)
    items = []
    for i in range(n):
        OPS += 1 # cálculo de razão
        if wt[i] <= 0:
            # evita divisão por zero; trata itens de peso zero como razão muito alta
            ratio = float('inf')
        else:
            ratio = val[i] / wt[i]
        items.append((ratio, wt[i], val[i], i))

    # Ordena por razão decrescente
    # A complexidade de sort é O(n log n), vamos contar n log n como operações aproximadas
    import math
    if n > 0:
        OPS += int(n * math.log2(n))
    
    items.sort(key=lambda x: x[0], reverse=True)

    remaining = W
    total_value = 0
    chosen = []
    for ratio, w, v, idx in items:
        OPS += 1 # visita do item
        if w <= remaining:
            chosen.append(idx)
            remaining -= w
            total_value += v
        # não pode pegar mais se a capacidade estiver esgotada
        if remaining == 0:
            break

    return total_value

if __name__ == "__main__":
    val = [1, 2, 3]
    wt = [4, 5, 1]
    W = 4
    
    print(knapsack(W, val, wt))
    print(f"Operações: {OPS}")