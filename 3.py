#[Better Approach 2] Using Bottom-Up DP (Tabulation) - O(n x W) Time and Space
#[Approximation] Greedy approach (value/weight ratio) - O(n log n) time
def knapsack(W, val, wt):
    """
    Greedy approximation for 0/1 knapsack: sort items by value/weight
    ratio and pick while capacity allows. This is not optimal in general
    but is fast and useful for large instances.

    Returns the total value of the chosen items.
    """
    n = len(val)
    items = []
    for i in range(n):
        if wt[i] <= 0:
            # avoid division by zero; treat zero-weight items as very high ratio
            ratio = float('inf')
        else:
            ratio = val[i] / wt[i]
        items.append((ratio, wt[i], val[i], i))

    # Sort by descending ratio
    items.sort(key=lambda x: x[0], reverse=True)

    remaining = W
    total_value = 0
    chosen = []
    for ratio, w, v, idx in items:
        if w <= remaining:
            chosen.append(idx)
            remaining -= w
            total_value += v
        # can't pick more if capacity is exhausted
        if remaining == 0:
            break

    return total_value

if __name__ == "__main__":
    val = [1, 2, 3]
    wt = [4, 5, 1]
    W = 4
    
    print(knapsack(W, val, wt))