import sys
format1 = {"fix":'c4', "float":'co', "hio":'f4', "norm":'c8', "sio":'f0', "tio":'f8'}

format2 = {
    "addr":'90', "clear":'b4', "divr":'9c', "compr":'a0', "mulr":'98', "rmo":'ac',
    "shiftl":'a4', "shiftr":'a8', "subr":'94', "svc":'b0', "tixr":'b8'
}

format34 = {
    "add":'18', "addf":'58', "and":'40', "comp":'28', "compf":'88', "div":'24', "divf":'64', "j":'3c', "jeq":'30',
    "jgt":'34', "jlt":'38', "jsub":'48' , "lda":'00', "ldb":'68', "ldch":'50', "ldf":'70', "ldl":'08',
    "lds":'6c', "ldt":'74', "ldx":'04', "lps":'d0', "mul":'20', "mulf":'60', "or":'or', "rd":'d8', "rsub":'4c',
    "td":'e0', "tix":'2c', "wd":'dc', "ssk":'ec', "sta":'0c', "stb":'78',   "stch":'54', "stf":'80', "sti":'d4',
    "stl":'14', "sts":'7c', "stsw":'e8', "stt":'84', "stx":'10', "sub":'1c',"subf":'5c'
}
