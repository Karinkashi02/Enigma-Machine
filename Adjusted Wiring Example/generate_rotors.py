import random

alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"

def create_valid_rotor():
    chars = list(alph)
    random.shuffle(chars)
    return ''.join(chars)

# Generate 2 new valid rotors
print("// rotor 2 - Fixed")
rotor2 = create_valid_rotor()
print(f'    "{rotor2}",')

# Verify it's valid
if len(rotor2) == len(alph) and len(set(rotor2)) == len(alph):
    print("    ✓ Valid")

print()

print("// rotor 4 - Fixed")
rotor4 = create_valid_rotor()
print(f'    "{rotor4}",')

# Verify it's valid
if len(rotor4) == len(alph) and len(set(rotor4)) == len(alph):
    print("    ✓ Valid")
