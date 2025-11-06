alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"

reflectors = [
    "ejmzalyxivhtfcgukpnwbrodqs57318206.,:; )(]['\"-+/*&~`!@#$%^_={}|\\<>?",
    "yrpiuksjlvhgfcdtoqenwbxamz64209317.,:; )(]['\"-+/*&~`!@#$%^_={}|\\<>?",
    "fvpnjaekmydsxirtcwzoqbgluh18309254.,:; )(]['\"-+/*&~`!@#$%^_={}|\\<>?",
    "ixdlpfaswtrmujknyohbqegzcv27418305.,:; )(]['\"-+/*&~`!@#$%^_={}|\\<>?"
]

for idx, refl in enumerate(reflectors, 1):
    print(f"\nReflector {idx}:")
    print(f"  Length: {len(refl)}")
    
    errors = []
    for i in range(len(alph)):
        char_in = alph[i]
        char_out = refl[i]
        
        # Check reverse mapping
        reverse_idx = alph.index(char_out)
        reverse_out = refl[reverse_idx]
        
        if reverse_out != char_in:
            errors.append(f"    {char_in}->{char_out} but {char_out}->{reverse_out} (should be {char_in})")
    
    if errors:
        print(f"  ✗ Found {len(errors)} symmetry errors:")
        for e in errors[:10]:
            print(e)
    else:
        print(f"  ✓ Properly symmetrical!")
