pb = "badcfehgjilknmporqtsvuxwzy1032546789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"
alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"

print("Checking plugboard symmetry:")
print(f"Length pb: {len(pb)}, alph: {len(alph)}")

errors = []
for i in range(len(alph)):
    char_in = alph[i]
    char_out = pb[i]
    if char_in != char_out:  # It's swapped
        # Check if the reverse is also true
        reverse_idx = alph.index(char_out)
        reverse_out = pb[reverse_idx]
        if reverse_out != char_in:
            errors.append(f"  {char_in}->{char_out} but {char_out}->{reverse_out} (should be {char_in})")

if errors:
    print(f"\nFound {len(errors)} symmetry errors:")
    for e in errors[:20]:
        print(e)
else:
    print("\n✓ Plugboard is properly symmetrical!")
