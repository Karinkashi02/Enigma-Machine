/***************************************************************************
 * ENIGMA.CPP - A simulator for the WW II cryptographic machine ENIGMA
 * 
 * Based on the article by Jorge Luis Orejel
 * Adapted from Chapter 12 of "Applied Algorithms and Data Structures"
 * 
 * This simulator implements a 3-4 rotor ENIGMA machine with plugboard
 * and reflector, supporting extended ASCII character set.
 ***************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// ========================================================================
// CONSTANTS AND DEFINITIONS
// ========================================================================

#define Nchars 69  // Total number of encipherable characters
#define Mchars 70  // Buffer size for strings containing Nchars
#define Nrotors 11 // Maximum number of rotors (1-based: 1-10)
#define Nrefls 5   // Total number of reflectors (1-based: 1-4)
#define Nsteps 11  // Maximum total number of encryption steps
                   // = 2*4 (rotors) + 2 (plugboard) + 1 (reflector)

#define Nline 255  // Maximum line length

// ========================================================================
// ROTOR AND REFLECTOR WIRINGS
// ========================================================================

char *ROTOR[Nrotors] = {
    // input alphabet ("rotor" 0, not used)
    "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?",
    // rotor 1 - New
    "(etazr'=in/%_m?b!c<#s42&{y;u\"80[7`k]d@j.)}o+-:3w lh>x9pf~qv5g|^6,*\\1$",
    // rotor 2 - New
    "w\"on,&`9hs$gu[=k3'p0:q!5;.*{/fiex+]~ya>|d%7b#\\_t}vm)r@2-l8<z6c(?4j 1^",
    // rotor 3 - New
    ">t\"6+8/eu@;}yi&m*24#_n5-%`,?a(h:!rzb[jk l7w'pd9]^sv3q{).cf$gx=0<o\\|~1",
    // rotor 4 - New
    "ae7o(yk-^}*5u)di8']fqb,~r063[m`$1!/l9wvhg{js:#n2z>tc@|=_+.;&<% \"\\?p4x",
    // rotor 5 - New
    "$t<l4&r`7wk-]} %y,o!iq.9^*e0jvzs_:b8{mx5+|f()[1'c=?/h>63au~\"#g\\;2d@pn",
    // rotor 6 - New
    "@ckmv=,wy(i`rz5+?]~>\\$)1![-n^u}0tq8_'9h/dj%ep:4gx2 7.|a<&6fo*b\";#sl{3",
    // rotor 7 - New
    "d]_ifj~u@rkax>1v-!{\"6* .}:b;)8'(c\\0zgo^,/4&=hq3w<m$#n9y[%52et?l+s|p`7",
    // rotor 8 - New
    "|#p4h.x}e9i~tvc,{'<w*:]-0>^b2`l\\on@$)&57au8+(yrqs;m1z3\"g!=jd6k[f% /?_",
    // rotor 9 (beta) - New
    "v.wze\" `ml'{qc;u-81:#s2h3f*)?%a,&=g+7]kb_r$}^i/(!\\p@o>d<~9j[0t5nx|4y6",
    // rotor 10 (gamma) - New
    "u\\={.!)z4?cg/pxi,;ad2#1[t(wv:5<h6@l>&`9f$38q%\"s*mok}bnr|~7] ^_ey+-j0'"
};
    // rotor 6 - Modified
    "qwertyuiopasdfghjklzxcvbnm6(8- \":1*)37;9&[5.2]/,40'+?><\\|}{=^_%$#@!`~",
    // rotor 7 - Modified
    "plokimjunhybgtvfrcedxwszaq;&410[8/:*]+3 \"926-,(7.)5'?><\\|}{=^_%$#@!`~",
    // rotor 8 - Modified
    "mnbvcxzaqwertyuioplkjhgfds2.)4',/ 836](9&[1:7+;5\"*0-?><\\|}{=^_%$#@!`~",
    // beta rotor - Modified
    "zyxwvutsrqponmlkjihgfedcba,7*6-5;2/+(3):8['1.&49\"0 ]?><\\|}{=^_%$#@!`~",
    // gamma rotor - Modified
    "qazwsxedcrfvtgbyhnujmikolp9] .2;\"7[4:3'6*8+,)(&/-510?><\\|}{=^_%$#@!`~"
};

// Position in which each rotor causes its left neighbor to turn
char NOTCH[Nrotors] = { 'z', 'm', 'r', 'f', 'w', 'k', 'p', 'l', 'n', 'd', 'g' };

char *REFLECTOR[Nrefls] = {
    // input alphabet ("REFLECTOR" 0, not used)
    "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?",
    // reflector B, thick - Properly symmetrical (auto-generated)
    "q8ercj}ltfnh&k2;aduisy 'v\"{4o#1%9=b6$~^pw]@\\(xz`+?<m,-|)3.5:>70g![*_/",
    // reflector C, thick - Properly symmetrical (auto-generated)
    "~$g7&4c3;xyq'[6tl vp|s.jk1%z?hf)od>_w\\/ir^5n\"m]#+:!ea{*=-b0(9@`<u,}82",
    // reflector B, dunn - Properly symmetrical (auto-generated)
    "l]n?58v*my+aic<0-.z|9g@>jsp/ `)e\"=fur{&$2^4'b[6qk1h:}3#w!;\\(_7,~t%oxd",
    // reflector C, dunn - Properly symmetrical (auto-generated)
    "^_1@%m6p/0*{fu<h) x\"n3:s5+jc}v[yg-|(]&w#r9q4.'t7zik,!?~d;=eab$l28>o\\`"
};

char *PLUGBOARD = "badcfehgjilknmporqtsvuxwzy1032546789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?";
char *alphabet = "abcdefghijklmnopqrstuvwxyz0123456789.,:; ()[]'\"-+/*&~`!@#$%^_={}|\\<>?";

// ========================================================================
// GLOBAL VARIABLES
// ========================================================================

int mRotors;                // Number of rotors placed in the machine (1-based: 1-4)
int mSteps;                 // Actual number of encryption steps
int RotPos[Nrotors];        // Rotor placed in each position
char window[Nrotors];       // Characters in window
char Iwindow[Nrotors];      // Initial values in 'window' (for resetting)
char *RotWiring[Nrotors];   // Rotor wirings
char RotNotch[Nrotors];     // Rotor switching positions
int RotNumber[Nrotors];     // Which physical rotor (t,1-8,b,g)
char *reflector;            // Wiring of the reflector
char plugboard[Mchars];     // Wirings of the plugboard
int ReflType;               // Reflector used
char step[Nsteps];          // Array to store encryption steps

// Files and variables for setup and reporting
FILE *inFp, *outFp, *logFp;
char inLine[Nline];
char outLine[Nline];

// ========================================================================
// FUNCTION PROTOTYPES
// ========================================================================

void InitEnigma();
void TryUserSetup();
void ProcessFile(char *inFname, char *encFname, char *logFname);
void reset();
int OpenFiles(char *inFname, char *encFname, char *logFname);
void CloseFiles();
void ReportMachine();
void ShowRotors();
void SetPlugboard();
void SetRotorsAndReflector();
int index(char c);
int ChrToInt(char c);
void PlaceRotor(int position, int r);
void SetRotorPositions();
int mod(int n, int modulus);
void ProcessPlainText();
void ShowWindow();
void ShowSteps();
char encrypt(char c);
void turn();
void TurnRot(int n, int width);
char RtoLpath(char c, int r);
char LtoRpath(char c, int r);

// ========================================================================
// UTILITY FUNCTIONS
// ========================================================================

int mod(int n, int modulus)
{
    while (n >= modulus)
        n -= modulus;
    while (n < 0)
        n += modulus;
    return n;
}

int index(char c)
{
    int i = 0;
    while ((i < Nchars) && (c != alphabet[i]))
        ++i;
    return i;
}

int ChrToInt(char c)
{
    return (int)(c - '0');
}

// ========================================================================
// INITIALIZATION FUNCTIONS
// ========================================================================

void InitEnigma()
{
    int i;

    mRotors = 3;
    mSteps = (mRotors << 1) + 3;
    strcpy(plugboard, PLUGBOARD);
    for (i = 0; i <= mRotors; ++i) {
        RotWiring[i] = ROTOR[i];
        RotNotch[i] = NOTCH[i];
        RotNumber[i] = i;
        Iwindow[i] = window[i] = 'a';
    }
    reflector = REFLECTOR[1];
    ReflType = 1;
}

void TryUserSetup()
{
    if ((inFp = fopen("esetup", "rt")) != NULL) {
        SetPlugboard();
        SetRotorsAndReflector();
        fclose(inFp);
    }
}

void SetPlugboard()
{
    int i, n, x;
    char p1, p2, ch;

    fgets(inLine, Nline, inFp);
    inLine[strlen(inLine) - 1] = '\0';
    n = strlen(inLine);

    for (i = 0; i < n; i += 2) {
        p1 = inLine[i];
        p2 = inLine[i + 1];
        x = index(p1);
        if ((ch = plugboard[x]) != p1) {
            plugboard[index(ch)] = ch;
            plugboard[x] = p1;
        }
        plugboard[x] = p2;
        x = index(p2);
        if ((ch = plugboard[x]) != p2) {
            plugboard[index(ch)] = ch;
            plugboard[x] = p1;
        }
        plugboard[x] = p1;
    }
}

void SetRotorsAndReflector()
{
    int i, n, rotor, rotPos;
    char ch, ringPos;

    fgets(inLine, Nline, inFp);
    mRotors = ChrToInt(inLine[0]);
    if (mRotors > 4)
        mRotors = 4;
    mSteps = (mRotors << 1) + 3;
    
    for (i = 1; i <= mRotors; ++i) {
        fgets(inLine, Nline, inFp);
        ch = inLine[0];
        if (isdigit((int)ch))
            rotor = ChrToInt(ch);
        else {
            ch = tolower(ch);
            rotor = ch == 'b' ? 9 : ch == 'g' ? 10 : 0;
        }
        rotPos = ChrToInt(inLine[1]);
        ringPos = inLine[2];
        Iwindow[rotPos] = window[rotPos] = ringPos;
        PlaceRotor(rotPos, rotor);
    }

    fgets(inLine, Nline, inFp);
    ch = inLine[0];
    switch (ch) {
        case 't': n = 0; break;
        case 'b': n = 1; break;
        case 'c': n = 2; break;
        case 'B': n = 3; break;
        case 'C': n = 4; break;
        default: n = 0; break;
    }
    reflector = REFLECTOR[n];
    ReflType = n;
}

void PlaceRotor(int position, int r)
{
    RotWiring[position] = ROTOR[r];
    RotNotch[position] = NOTCH[r];
    RotNumber[position] = r;
}

void SetRotorPositions()
{
    int i, j, k;
    char *Rwiring, ch;

    for (i = 1; i <= mRotors; ++i) {
        j = RotNumber[i];
        ch = window[j];
        Rwiring = RotWiring[j];
        k = 0;
        while (Rwiring[k] != ch)
            ++k;
        RotPos[j] = k;
    }
}

void reset()
{
    for (int i = 1; i <= mRotors; ++i)
        window[i] = Iwindow[i];
}

// ========================================================================
// FILE OPERATIONS
// ========================================================================

int OpenFiles(char *inFname, char *encFname, char *logFname)
{
    inFp = fopen(inFname, "rt");
    outFp = fopen(encFname, "wt");
    logFp = fopen(logFname, "wt");
    return (inFp != NULL) && (outFp != NULL) && (logFp != NULL);
}

void CloseFiles()
{
    fclose(inFp);
    fclose(outFp);
    fclose(logFp);
}

// ========================================================================
// REPORTING FUNCTIONS
// ========================================================================

void ReportMachine()
{
    fprintf(logFp, "Plugboard mappings:\n");
    fprintf(logFp, "%s\n", ROTOR[0]);
    fprintf(logFp, "%s\n", plugboard);

    fprintf(logFp, "\nRotor wirings:\n");
    fprintf(logFp, "position rotor ring setting notch sequence\n");
    for (int i = mRotors; i >= 1; --i)
        fprintf(logFp, "%8d %5d %12c %5c %s\n",
                i, RotNumber[i], window[i],
                RotNotch[i], RotWiring[i]);
    fprintf(logFp, "\nreflector %d %s\n", ReflType, reflector);
    fprintf(logFp, "\nrotors:\n");
    ShowRotors();
}

void ShowRotors()
{
    int i, j, k;
    char *Rwiring;

    for (i = mRotors; i >= 1; --i) {
        fprintf(logFp, "%d: ", i);
        Rwiring = RotWiring[i];
        k = RotPos[i];
        for (j = 0; j < k; ++j)
            fprintf(logFp, "%c", *Rwiring++);
        fprintf(logFp, "->");
        for (j = k; j < Nchars; ++j)
            fprintf(logFp, "%c", *Rwiring++);
        fprintf(logFp, "\n");
    }
}

void ShowWindow()
{
    for (int i = mRotors; i >= 1; --i)
        fprintf(logFp, "%c ", window[i]);
    fprintf(logFp, "  ");
}

void ShowSteps()
{
    for (int i = 0; i < mSteps; ++i)
        fprintf(logFp, " -> %c", step[i]);
}

// ========================================================================
// ENCRYPTION CORE
// ========================================================================

void TurnRot(int n, int width)
{
    char *r;

    if (width > 0) {
        RotPos[n] = mod(RotPos[n] + width, Nchars);
        r = RotWiring[n];
        window[n] = r[RotPos[n]];
    }
}

void turn()
{
    int i, doit[Nrotors];
    char *r1 = RotWiring[1], *r2 = RotWiring[2], *r3;

    if (mRotors > 3)
        r3 = RotWiring[3];

    // Calculate stepwidth for each rotor
    doit[1] = 1;
    for (i = 2; i <= mRotors; ++i)
        doit[i] = 0;
    
    if ((RotNotch[1] == r1[RotPos[1]]) ||
        (RotNotch[2] == r2[RotPos[2]]))  // double stepping
        doit[2] = 1;
    
    if (RotNotch[2] == r2[RotPos[2]])
        doit[3] = 1;
    
    if (mRotors > 3) {
        if (RotNotch[3] == r3[RotPos[3]])
            doit[4] = 1;
    }

    // Turn rotors "simultaneously"
    for (int n = 1; n <= mRotors; ++n)
        TurnRot(n, doit[n]);
}

char RtoLpath(char c, int r)
{
    int n, offset, idx, ret;
    char *CurRotor;

    CurRotor = RotWiring[r];
    n = index(c);
    offset = index(CurRotor[RotPos[r]]);
    idx = mod(n + offset, Nchars);
    ret = mod(index(CurRotor[idx]) - offset, Nchars);
    return alphabet[ret];
}

char LtoRpath(char c, int r)
{
    int n, m, offset, idx, newchar;
    char *CurRotor;

    CurRotor = RotWiring[r];
    n = index(c);
    offset = index(CurRotor[RotPos[r]]);
    newchar = alphabet[mod(n + offset, Nchars)];

    m = 0;
    while (m < Nchars && CurRotor[m] != newchar)
        ++m;
    idx = mod(m - offset, Nchars);
    return alphabet[idx];
}

char encrypt(char c)
{
    int i, r;

    turn();                                          // move rotors
    i = 0;                                           // pass through:
    step[i++] = plugboard[index(c)];                 //    plugboard
    for (r = 1; r <= mRotors; ++r)
        step[i++] = RtoLpath(step[i - 1], r);        //    right-to-left path
    step[i++] = reflector[index(step[i - 1])];       //    reflector
    for (r = mRotors; r >= 1; --r)                   //    left-to-right path
        step[i++] = LtoRpath(step[i - 1], r);
    step[i] = plugboard[index(step[i - 1])];         //    plugboard

    return step[i];
}

// ========================================================================
// TEXT PROCESSING
// ========================================================================

void ProcessPlainText()
{
    int i, n;
    char c1, c2;

    fprintf(logFp, "\n\nEncryption\n");
    while (fgets(inLine, Nline, inFp) != NULL) {

        n = strlen(inLine);
        // Remove newline character if present
        if (n > 0 && inLine[n - 1] == '\n') {
            inLine[n - 1] = '\0';
            n--;
        }

        for (i = 0; i < n; ++i) {
            c1 = inLine[i];
            if (isupper((int)c1))
                c1 = tolower(c1);

            c2 = encrypt(c1);

            // ShowRotors();
            ShowWindow();
            fprintf(logFp, " %c", c1);
            ShowSteps();
            fprintf(logFp, "\n");
            outLine[i] = c2;
        }
        fprintf(logFp, "\n");
        outLine[i] = '\0';
        fprintf(outFp, "%s\n", outLine);
    }
}

void ProcessFile(char *inFname, char *encFname, char *logFname)
{
    if (OpenFiles(inFname, encFname, logFname)) {
        SetRotorPositions();
        ReportMachine();
        ProcessPlainText();
        CloseFiles();
    }
}

// ========================================================================
// MAIN FUNCTION
// ========================================================================

int main()
{
    printf("ENIGMA Simulator - Starting...\n");
    
    InitEnigma();
    TryUserSetup();

    printf("Encrypting 'plain' -> 'encrypt'...\n");
    ProcessFile("plain", "encrypt", "elog");
    
    reset();
    
    printf("Decrypting 'encrypt' -> 'decrypt'...\n");
    ProcessFile("encrypt", "decrypt", "dlog");

    printf("Done! Check output files: encrypt, decrypt, elog, dlog\n");
    
    return 0;
}
