from FooProg import *
import sys,time,json,os
a=sys.argv
def show(x):
    return ('%.20lf' % x).rstrip('0').rstrip('.')
if len(a)<3:
    print('Fooprog needs at least 2 arguments')
    sys.exit(-1)
if not os.path.exists(a[2]):
    print(f'File {a[2]} does not exist.')
    sys.exit(-2)
match a[1]:
    case 'c':
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
    case _:
        print('Invalid argument %s:\n - "c" for tokenizing and compiling a source\n - "t" for just tokenizing'%a[1])