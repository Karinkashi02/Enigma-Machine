alph = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"
print(f"Alphabet: {len(alph)} chars\n")

# Check plugboard
plugboard = "badcfehgjilknmporqtsvuxwzy1032546789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?"
print("PLUGBOARD:")
print(f"  Length: {len(plugboard)}")
errors = 0
for i in range(len(alph)):
    char_in = alph[i]
    char_out = plugboard[i]
    if char_in != char_out:
        reverse_idx = alph.index(char_out)
        reverse_out = plugboard[reverse_idx]
        if reverse_out != char_in:
            print(f"  ✗ {char_in}->{char_out} but {char_out}->{reverse_out}")
            errors += 1
if errors == 0:
    print(f"  ✓ Symmetrical")
else:
    print(f"  ✗ {errors} errors")

# Check reflectors
reflectors = [
    ("Reflector 1", "q8ercj}ltfnh&k2;aduisy 'v\"{4o#1%9=b6$~^pw]@\\(xz`+?<m,-|)3.5:>70g![*_/"),
    ("Reflector 2", "~$g7&4c3;xyq'[6tl vp|s.jk1%z?hf)od>_w\\/ir^5n\"m]#+:!ea{*=-b0(9@`<u,}82"),
    ("Reflector 3", "l]n?58v*my+aic<0-.z|9g@>jsp/ `)e\"=fur{&$2^4'b[6qk1h:}3#w!;\\(_7,~t%oxd"),
    ("Reflector 4", "^_1@%m6p/0*{fu<h) x\"n3:s5+jc}v[yg-|(]&w#r9q4.'t7zik,!?~d;=eab$l28>o\\`"),
]

for name, refl in reflectors:
    print(f"\n{name}:")
    print(f"  Length: {len(refl)}")
    errors = 0
    for i in range(min(len(alph), len(refl))):
        char_in = alph[i]
        char_out = refl[i]
        try:
            reverse_idx = alph.index(char_out)
            reverse_out = refl[reverse_idx]
            if reverse_out != char_in:
                errors += 1
        except:
            errors += 1
    if errors == 0:
        print(f"  ✓ Symmetrical")
    else:
        print(f"  ✗ {errors} errors")
