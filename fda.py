from FooProg import *
import sys
a=sys.argv
if len(a)!=2:
    print('FDA Needs 2 arguments!')
    sys.exit(-1)
try:
    with open(a[1],'rb') as f:
        x=f.read()
except:
    print('Cannot open given FooProg binary')
    sys.exit(-3)
y=disasm(x)
if not y:
    sys.exit(-2)
else:
    for i in y:
        print('%05x'%i[1],'\t',i[0],'\t',x[i[1]:i[2]].hex(' '))