#!/usr/bin/env python3
"""
Verify the solution and explore the problem space.
"""

arr = [1, 2, 3, 2, 3, 4, 3, 4]

print("Array:", arr)
print("\nChecking if the entire array is valid:")
print()

for i in range(len(arr) - 1):
    diff = abs(arr[i] - arr[i+1])
    print(f"Position {i} to {i+1}: {arr[i]} -> {arr[i+1]}, |diff| = {diff}")

print("\n" + "="*50)
print("VERIFICATION:")
print("="*50)

all_valid = True
for i in range(len(arr) - 1):
    diff = abs(arr[i] - arr[i+1])
    if diff != 1:
        all_valid = False
        print(f"❌ Invalid at position {i}: |{arr[i]} - {arr[i+1]}| = {diff}")

if all_valid:
    print("✓ All adjacent pairs have difference of exactly 1!")
    print(f"✓ The entire array of length {len(arr)} is the answer!")
