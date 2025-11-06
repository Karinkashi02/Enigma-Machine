import random

alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"

print(f"// All {len(alph)} chars")
for i in range(1, 11):
    chars = list(alph)
    random.shuffle(chars)
    rotor = ''.join(chars)
    print(f'    // rotor {i} - New')
    print(f'    "{rotor}",')
