from FooProg import *
import sys,time,json,os
a=sys.argv
def show(x):
    return ('%.20lf' % x).rstrip('0').rstrip('.')
def helper():
    print('fooprog <command>:\n - "c <file>" for tokenizing and compiling a source\n - "t <file>" for just tokenizing\n - "i <file>" for interpreting bytecode\n - "d <file>" for disassembling\n - "v" for version\n - "h" for help')
if len(a)==1:
    helper()
    sys.exit(0)
match a[1]:
    case 'c':
        if len(a)!=3:
            helper()
            sys.exit(0)
        if not os.path.exists(a[2]):
            print(f'File {a[2]} does not exist.')
            sys.exit(-2)
        with open(a[2],'r',encoding='ansi',errors='replace') as f:
            n=f.read()
        print('Tokenizing...')
        t=time.perf_counter()
        x=tokenize(n)
        if isinstance(x,int):
            print('Tokenization failed with return code %d'%x)
            sys.exit(x)
        else:
            print(f'Tokenization ran successfully in {show(time.perf_counter()-t)} secs')
            print('Compiling...')
            t=time.perf_counter()
            bk=tobk(x)
            if isinstance(bk,int):
                print('Compilation failed with return code %d'%x)
                sys.exit(x)
            else:
                print(f'Compilation ran successfully in {show(time.perf_counter()-t)} secs')
                with open(a[2]+'.fb','wb') as fw:
                    fw.write(bk)
                print('Successfully saved compiled program as %s'%(a[2]+'.fb'))
    case 't':
        if len(a)!=3:
            helper()
            sys.exit(0)
        if not os.path.exists(a[2]):
            print(f'File {a[2]} does not exist.')
            sys.exit(-2)
        with open(a[2],'r',encoding='ansi',errors='replace') as f:
            n=f.read()
        print('Tokenizing...')
        t=time.perf_counter()
        x=tokenize(n)
        if isinstance(x,int):
            print('Tokenization failed with return code %d'%x)
            sys.exit(x)
        else:
            print(f'Tokenization ran successfully in {show(time.perf_counter()-t)} secs')
            with open(a[2]+'.json','w') as fq:
                json.dump(x,fq)
            print('Successfully saved tokens as %s'%(a[2]+'.json'))
    case 'i':
        if len(a)!=3:
            helper()
            sys.exit(0)
        if not os.path.exists(a[2]):
            print(f'File {a[2]} does not exist.')
            sys.exit(-2)
        if not os.path.exists(sys.argv[2]):
            print(f'File {sys.argv[2]} does not exist.')
            sys.exit(-2)
        with open(sys.argv[2],'rb') as f:
                x=f.read()
        rs=runbk(x)
        if isinstance(rs,int):
            sys.exit(rs)
        else:
            sys.exit(0)
    case 'd':
        if len(a)!=3:
            helper()
            sys.exit(0)
        if not os.path.exists(a[2]):
            print(f'File {a[2]} does not exist.')
            sys.exit(-2)
        if not os.path.exists(sys.argv[2]):
            print(f'File {sys.argv[2]} does not exist.')
            sys.exit(-2)
        with open(sys.argv[2],'rb') as f:
                x=f.read()
        y=disasm(x)
        if not y:
            sys.exit(-1)
        else:
            for i in y:
                print('%05x'%i[1],'\t',i[0],'\t',x[i[1]:i[2]].hex(' '))
    case 'v':
        print(f'FooProg all-in-one version {version}')
    case _:
        helper()
