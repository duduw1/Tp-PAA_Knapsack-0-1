# [Abordagem Ingênua] Usando Recursão O(2^n) Tempo e O(n) Espaço
# Retorna o valor máximo que pode ser colocado em uma mochila de capacidade W

# Variável global para contar operações (chamadas recursivas)
OPS = 0

def knapsackRec(W, val, wt, n):
    global OPS
    OPS += 1

    # Caso Base: se não houver itens ou capacidade, o valor é 0
    if n == 0 or W == 0:
        return 0

    pick = 0

    # Escolhe o n-ésimo item se ele não exceder a capacidade da mochila
    if wt[n - 1] <= W:
        pick = val[n - 1] + knapsackRec(W - wt[n - 1], val, wt, n - 1)
    
    # Não escolhe o n-ésimo item
    notPick = knapsackRec(W, val, wt, n - 1)
     
    # Retorna o máximo entre escolher ou não o item
    return max(pick, notPick)

def knapsack(W, val, wt):
    global OPS
    OPS = 0
    n = len(val)
    return knapsackRec(W, val, wt, n)

if __name__ == "__main__":
    val = [1, 2, 3]
    wt = [4, 5, 1]
    W = 4

    print(knapsack(W, val, wt))
    print(f"Operações: {OPS}")