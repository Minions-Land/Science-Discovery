from itertools import permutations

def has_adjacent_duplicates(arrangement):
    """Check if arrangement has any adjacent identical letters"""
    for i in range(len(arrangement) - 1):
        if arrangement[i] == arrangement[i + 1]:
            return True
    return False

# Generate all unique permutations of A, A, B, B, C, C, D
letters = ['A', 'A', 'B', 'B', 'C', 'C', 'D']

# Get all unique permutations
unique_perms = set(permutations(letters))

print(f"Total unique arrangements: {len(unique_perms)}")

# Count arrangements without adjacent duplicates
valid_count = 0
for perm in unique_perms:
    if not has_adjacent_duplicates(perm):
        valid_count += 1

print(f"Arrangements without adjacent duplicates: {valid_count}")

# Verify our calculation
print("\nVerification of inclusion-exclusion:")
print(f"Total arrangements: 7!/(2!*2!*2!) = {5040//8}")
print(f"Expected answer: {630 - 384}")
print(f"Computed answer: {valid_count}")
print(f"Match: {valid_count == 246}")