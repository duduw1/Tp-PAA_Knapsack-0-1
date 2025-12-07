"""
Dynamic programming 0/1 knapsack with item reconstruction.

Provides two functions:
- `knapsack(W, val, wt)` -> returns maximum total value (int) (keeps compatibility)
- `knapsack_with_items(W, val, wt)` -> returns (total_value, chosen_indices)

When run as a script, demonstrates the algorithm and prints which items were
chosen (by index) and the total value.
"""

def knapsack_with_items(W, val, wt):
	"""
	Bottom-up DP for 0/1 knapsack that also reconstructs the chosen items.

	Returns a tuple (max_value, chosen_indices) where chosen_indices is a list
	of item indices (0-based) that were selected to achieve max_value. The
	reconstruction prefers higher-index items first when ties occur because of
	the backtracking order.
	"""
	n = len(val)
	# dp[i][w] = max value using first i items (items 0..i-1) with capacity w
	dp = [[0] * (W + 1) for _ in range(n + 1)]

	for i in range(1, n + 1):
		vi = val[i - 1]
		wi = wt[i - 1]
		for w in range(0, W + 1):
			if wi <= w:
				# pick or not pick
				pick = vi + dp[i - 1][w - wi]
				not_pick = dp[i - 1][w]
				dp[i][w] = max(pick, not_pick)
			else:
				dp[i][w] = dp[i - 1][w]

	# Reconstruct chosen items
	chosen = []
	w = W
	for i in range(n, 0, -1):
		if dp[i][w] != dp[i - 1][w]:
			# item i-1 was taken
			chosen.append(i - 1)
			w -= wt[i - 1]
			if w <= 0:
				break

	chosen.reverse()
	return dp[n][W], chosen


def knapsack(W, val, wt):
	"""Compatibility wrapper that returns only the max value (int)."""
	max_val, _ = knapsack_with_items(W, val, wt)
	return max_val


if __name__ == '__main__':
	# Demo example
	val = [1, 2, 3]
	wt = [4, 5, 1]
	W = 4

	total, items = knapsack_with_items(W, val, wt)
	print(f"Max value: {total}")
	print(f"Chosen item indices: {items}")
