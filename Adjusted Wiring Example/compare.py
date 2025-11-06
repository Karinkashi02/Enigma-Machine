with open('plain', 'r') as f:
    plain = f.read()

with open('decrypt', 'r') as f:
    decrypt = f.read()

print("Plain length:", len(plain))
print("Decrypt length:", len(decrypt))

# Find differences
print("\nDifferences (first 50):")
count = 0
for i, (p, d) in enumerate(zip(plain, decrypt)):
    if p != d:
        print(f"  Position {i}: '{p}' != '{d}'")
        count += 1
        if count >= 50:
            break

print(f"\nTotal differences: {sum(1 for p, d in zip(plain, decrypt) if p != d)}")
