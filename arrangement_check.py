from itertools import permutations

def has_adjacent_duplicates(arrangement):
    """Check if arrangement has any adjacent identical letters"""
    for i in range(len(arrangement) - 1):
        if arrangement[i] == arrangement[i + 1]:
            return True
    return False

# Generate all unique permutations
letters = ['A', 'A', 'B', 'B', 'C', 'C', 'D']
all_perms = set(permutations(letters))

print(f"Total arrangements: {len(all_perms)}")

# Count valid arrangements (no adjacent duplicates)
valid_count = 0
for perm in all_perms:
    if not has_adjacent_duplicates(perm):
        valid_count += 1

print(f"Valid arrangements (no adjacent duplicates): {valid_count}")

# Verify our calculation
print(f"\nVerification:")
print(f"Total = 7!/(2!*2!*2!) = {5040//8} = 630")
print(f"Expected valid arrangements: 246")
print(f"Match: {valid_count == 246}")