# [Abordagem Esperada] Usando PD Bottom-Up (Espaço Otimizado) - O(n x W) Tempo e O(W) Espaço
# Função para encontrar o lucro máximo

# Variável global para contar operações (atualizações na tabela)
OPS = 0

def knapsack(W, val, wt):
    global OPS
    OPS = 0
    
    # Inicializando a lista dp com 0
    # dp[j] armazenará o valor máximo para a capacidade j
    dp = [0] * (W + 1)
    
    # Considerando os itens um por um
    for i in range(1, len(wt) + 1):
        
        # Percorrendo de trás para frente (de W até o peso do item atual)
        # Isso garante que estamos usando os dados da computação anterior (i-1 itens)
        # sem reutilizar o mesmo item na mesma iteração
        for j in range(W, wt[i - 1] - 1, -1):
            OPS += 1
            dp[j] = max(dp[j], dp[j - wt[i - 1]] + val[i - 1])
    
    return dp[W]

if __name__ == "__main__":
    val = [1, 2, 3]
    wt = [4, 5, 1]
    W = 4

    print(knapsack(W, val, wt))
    print(f"Operações: {OPS}")