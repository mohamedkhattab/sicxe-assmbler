import sys

format1 = ["fix", "float", "hio", "norm", "sio", "tio"]

format2 = [
    "addr", "clear", "divr", "compr", "mulr", "rmo",
    "shiftl", "shiftr", "subr", "svc", "tixr"
]

format34 = [
    "add", "addf", "and", "comp", "compf", "div", "divf", "j", "jeq",
    "jgt", "jlt", "jsub" , "lda", "ldb", "ldch", "ldf", "ldl",
    "lds", "ldt", "ldx", "lps", "mul", "mulf", "or", "rd", "rsub",
    "td", "tix", "wd", "ssk", "sta", "stb",   "stch", "stf", "sti",
    "stl", "sts", "stsw", "stt", "stx", "sub","subf"
]

variable = ["resw" , "resb" , "word" , "byte"]

sym_tab = {}
lit_tab = {}
fin_sym_tab = {}

PC = 0

def error(string):
    print(string)
    sys.exit(-1)

def readFile(fname):
    return [line[:-1] for line in open(fname).readlines()]

def tokenizeInstructions(instructions):
    tokens = []
    i = 0
    for inst in instructions:
        tokens.append( [token for token in inst.split(' ') if token != ''] )
        i += 1

    return tokens

def getMnemonic(inst):
    if len(inst) == 3:
        return inst[1]
    else:
        return inst[0]

def getOperand(inst):
    if len(inst) == 3:
        return inst[2]
    elif len(inst) == 2:
        return inst[1]

def literalToHex(literal):
    res = ""
    for c in literal:
        res += hex( ord( c ) )

    return res
    
def convertLiteral(literal, pc):
    h = literalToHex(literal[2:-1]).replace('0x', '')
    if not ( literal in lit_tab.values() ):
        lit_tab[literal] = [h, str( len(h)/2 ), hex(pc)]
    
def convertLiteralX(literal, pc):
    h = literal[2:-1]
    if not ( literal in lit_tab.values() ):
        lit_tab[literal] = [h, str( len(h)/2 ), hex(pc)]

def reserveMem(inst):
    global PC
    mnemonic = getMnemonic(inst).lower()
    
    if mnemonic == 'start':
        prog_start = getOperand(inst)
        sym_tab[prog_start] = inst
        PC = int(prog_start, 16)
    
    elif mnemonic in format1:
        sym_tab[hex(PC)] = inst
        PC += 0x1

    elif mnemonic in format2:
        sym_tab[hex(PC)] = inst
        PC += 0x2

    elif mnemonic in format34:
        if mnemonic[0] == '+':
            sym_tab[hex(PC)] = inst
            PC += 0x4
        else:
            sym_tab[hex(PC)] = inst
            PC += 0x3

    elif mnemonic == "resb":
        op = getOperand(inst)
        if op[0] == 'X':
            sym_tab[hex(PC)] = inst
            PC += int(op[2:-1], 16)
        elif op[0] == 'C':
            error("RESB does not support character literals at C'")
        else:
            sym_tab[hex(PC)] = inst
            PC += int(op)
            
    elif mnemonic == "byte":
        op = getOperand(inst)
        if op[0] == 'X':
            sym_tab[hex(PC)] = inst
            PC += int(op[2:-1], 16) * len(op[2:-1])
        elif op[0] == 'C':
            sym_tab[hex(PC)] = inst
            PC += len(op[2:-1])
        else:
            sym_tab[hex(PC)] = inst
            PC += 1

    elif mnemonic == "word":
        sym_tab[hex(PC)] = inst
        PC += 3

    elif mnemonic == "resw":
        op = getOperand(inst)
        if op[0] == 'X':
            sym_tab[hex(PC)] = inst
            PC += int(op[2:-1], 16) * 3
        elif op[0] == 'C':
            error("RESW does not support character literals at C'")
        else:
            sym_tab[hex(PC)] = inst
            PC += int(op) * 3
            
    elif mnemonic == "=":
        op = getOperand(inst)
        if op[0] == "C":
            convertLiteral(op, PC + 3)
        if op[0] == "X":
            convertLiteralX(op, PC + 3)
            
    elif mnemonic == ".":
        pass

def genFinSymTab():
    for key in sym_tab:
        inst = sym_tab[key]
        if len(inst) == 3:
            fin_sym_tab[inst[0]] = key
            
def pass1():
    if len(sys.argv) < 2:
        error("*No input file specified")
    else:
        insts = readFile( sys.argv[1] )
        tokens = tokenizeInstructions(insts)
        for token in tokens:
            reserveMem(token)
            
pass1()
genFinSymTab()

def printSymTab():
    for key in sym_tab:
        print(key + " " + ' '.join(sym_tab[key]))

def printLitTab():
    for key in lit_tab:
        print(key + " " + ' '.join(lit_tab[key]))

def printFinSymTab():
    for key in fin_sym_tab:
        print(key + " " + ''.join(fin_sym_tab[key]))


print("SYMBOL TABLE:")
print("")
printFinSymTab()

print("")
print("LITERAL TABLE:")
print("")
printLitTab()

print("")
print("INSTRUCTIONS:")
print("")
printSymTab()


