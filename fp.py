from FooProg import *
import sys,os
if len(sys.argv) < 2:
    print('Fooprog interpreter needs at least 1 argument')
    sys.exit(-1)
if not os.path.exists(sys.argv[1]):
    print(f'File {sys.argv[1]} does not exist.')
    sys.exit(-2)
with open(sys.argv[1],'rb') as f:
    x=f.read()
rs=runbk(x)
if isinstance(rs,int):
    sys.exit(rs)
else:
    sys.exit(0)