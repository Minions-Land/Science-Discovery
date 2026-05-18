#!/usr/bin/env python3
"""
Find the longest subsequence where adjacent elements differ by exactly 1.
"""

def find_longest_subsequence(arr):
    """
    Find the longest subsequence where |arr[i] - arr[i+1]| = 1 for all adjacent pairs.

    Approach: Dynamic Programming
    - dp[i][v] = longest subsequence ending at index i with value v
    - For each position, we can extend subsequences that ended with value v-1 or v+1
    """
    n = len(arr)
    if n == 0:
        return [], 0

    # dp[i] will store a dict: value -> (length, parent_index, parent_value)
    dp = [{} for _ in range(n)]

    # Initialize first element
    dp[0][arr[0]] = (1, -1, None)

    max_length = 1
    max_end_idx = 0
    max_end_val = arr[0]

    for i in range(1, n):
        val = arr[i]

        # Option 1: Start a new subsequence with just this element
        dp[i][val] = (1, -1, None)

        # Option 2: Extend previous subsequences
        # Look for subsequences ending with val-1 or val+1
        for j in range(i):
            for prev_val, (prev_len, _, _) in dp[j].items():
                if abs(val - prev_val) == 1:
                    new_len = prev_len + 1
                    # Update if this gives a longer subsequence
                    if val not in dp[i] or dp[i][val][0] < new_len:
                        dp[i][val] = (new_len, j, prev_val)

        # Track the maximum
        for val, (length, _, _) in dp[i].items():
            if length > max_length:
                max_length = length
                max_end_idx = i
                max_end_val = val

    # Reconstruct the subsequence
    subsequence = []
    idx = max_end_idx
    val = max_end_val

    while idx != -1:
        subsequence.append(arr[idx])
        length, parent_idx, parent_val = dp[idx][val]
        idx = parent_idx
        val = parent_val

    subsequence.reverse()
    return subsequence, max_length


def verify_subsequence(subseq):
    """Verify that all adjacent elements differ by exactly 1."""
    if len(subseq) <= 1:
        return True

    for i in range(len(subseq) - 1):
        if abs(subseq[i] - subseq[i+1]) != 1:
            return False
    return True


if __name__ == "__main__":
    arr = [1, 2, 3, 2, 3, 4, 3, 4]

    print(f"Input array: {arr}")
    print()

    subsequence, length = find_longest_subsequence(arr)

    print(f"Longest subsequence: {subsequence}")
    print(f"Length: {length}")
    print()

    # Verify the subsequence
    is_valid = verify_subsequence(subsequence)
    print(f"Valid (all adjacent diffs = 1): {is_valid}")

    if is_valid and len(subsequence) > 1:
        print("\nDifferences between adjacent elements:")
        for i in range(len(subsequence) - 1):
            diff = abs(subsequence[i] - subsequence[i+1])
            print(f"  |{subsequence[i]} - {subsequence[i+1]}| = {diff}")
