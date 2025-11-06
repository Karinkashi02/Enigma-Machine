alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"

rotors = [
    "wtoyguhqsldpxnvbkmiezcrafj3.:7,51)-&;' +*9/\"](264[08?><\\|}{=^_%$#@!`~",
    "kzgnjyhmqwxvlrdbutsafoeicpc298.]6[\"/3,5+':4)0&;(*1- 7?><\\|}{=^_%$#@!`~",
    "nxwqazmklpoiuhygtfredcvbsj02468,9(['/-&;*31+57.:\"]) ?><\\|}{=^_%$#@!`~",
    "thgfedcbazywvutsrqponmlkxij7] -(&21*)\"6[9/,;8'4.50:+3?><\\|}{=^_%$#@!`~",
    "ymsbflkgdaqwertpoiuxcvnhzj-&3[92'*\"(]5;1,/4+:6) 078.?><\\|}{=^_%$#@!`~",
    "qwertyuiopasdfghjklzxcvbnm6(8- \":1*)37;9&[5.2]/,40'+?><\\|}{=^_%$#@!`~",
    "plokimjunhybgtvfrcedxwszaq;&410[8/:*]+3 \"926-,(7.)5'?><\\|}{=^_%$#@!`~",
    "mnbvcxzaqwertyuioplkjhgfds2.)4',/ 836](9&[1:7+;5\"*0-?><\\|}{=^_%$#@!`~",
    "zyxwvutsrqponmlkjihgfedcba,7*6-5;2/+(3):8['1.&49\"0 ]?><\\|}{=^_%$#@!`~",
    "qazwsxedcrfvtgbyhnujmikolp9] .2;\"7[4:3'6*8+,)(&/-510?><\\|}{=^_%$#@!`~"
]

print(f"Alphabet length: {len(alph)}\n")

for i, rotor in enumerate(rotors, 1):
    print(f"Rotor {i}:")
    print(f"  Length: {len(rotor)}")
    
    # Check for duplicates
    char_counts = {}
    for c in rotor:
        char_counts[c] = char_counts.get(c, 0) + 1
    
    duplicates = {c: count for c, count in char_counts.items() if count > 1}
    missing = [c for c in alph if c not in rotor]
    
    if duplicates:
        print(f"  ✗ Duplicates found: {duplicates}")
    if missing:
        print(f"  ✗ Missing characters: {missing}")
    if not duplicates and not missing and len(rotor) == len(alph):
        print(f"  ✓ Valid permutation")
    
    print()
