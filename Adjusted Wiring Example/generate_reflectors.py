import random

alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"
print(f"Alphabet length: {len(alph)}")
print(f"Alphabet: {alph}")

def create_symmetrical_reflector():
    chars = list(alph)
    mapping = [''] * len(chars)
    
    while chars:
        # Pick two random characters and swap them
        if len(chars) == 1:
            # Odd number - map to itself
            c = chars[0]
            idx = alph.index(c)
            mapping[idx] = c
            chars.remove(c)
        else:
            c1 = random.choice(chars)
            chars.remove(c1)
            c2 = random.choice(chars)
            chars.remove(c2)
            
            # Create symmetric mapping
            idx1 = alph.index(c1)
            idx2 = alph.index(c2)
            mapping[idx1] = c2
            mapping[idx2] = c1
    
    return ''.join(mapping)

# Create 4 different reflectors
for i in range(4):
    refl = create_symmetrical_reflector()
    print(f"\nReflector {i+1}:")
    print(f'    "{refl}",')
    
    # Verify symmetry
    errors = 0
    for j in range(len(alph)):
        char_in = alph[j]
        char_out = refl[j]
        reverse_idx = alph.index(char_out)
        reverse_out = refl[reverse_idx]
        if reverse_out != char_in:
            errors += 1
    
    print(f"    Errors: {errors}, Length: {len(refl)}")
