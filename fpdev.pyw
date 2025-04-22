import sys, os, platform
from FooProg import keywords,operators,disasm,tobk,tokenize
from threading import Thread
from base64 import *
import time
from tkinter import *
from json import dumps
import tic
from tkinter.messagebox import *
from json import load,dump
from fdcdlg import *
main=tic.Main()
recentfilelist=[]
def show(x):
    return ('%.20lf' % x).rstrip('0').rstrip('.')
major_version = sys.version_info.major
if major_version == 2:
    sys.exit()
elif major_version == 3:
    from tkinter import *
    import tkinter.filedialog as tkFileDialog
    import tkinter.messagebox as tmb
else:
    sys.exit()
class PrintHooked():
    def __init__(self,txt):
        self.txt=txt
        self.normal=sys.stdout
    def write(self,val):
        self.txt.insert('end',val)
        self.txt.update()
def syn(code):
    l=[]
    it=0
    flag=False
    if not code.endswith(';'):
        code+=';'
        flag=True
    while(it<len(code)):
        try:
            if code[it]=='$':
                s='$'
                it+=1
                while code[it]!='$':
                    s+=code[it]
                    it+=1
                s+='$'
                l.append((s,'var'))
            elif code[it] in '0123456789.':
                if code[it] == "0":
                    if it==len(code)-1:
                        l += [("0", "number")]
                    elif code[it + 1] == "o":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        l += [('0o'+tmp, "oct")]
                    elif code[it + 1] == "x":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890ABCDEFabcdef":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        l += [('0x'+tmp.lower(), "hex")]
                    elif code[it + 1] == "b":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        l += [('0b'+tmp, "bin")]
                    else:
                        l += [("0", "number")]
                else:
                    tmp = ""
                    while it < len(code) and code[it] in "1234567890.":
                        tmp += code[it]
                        it += 1
                    it -= 1
                    l += [(tmp, "number")]
            elif code[it] in ';(){}':
                l+=[(code[it],"symbol")]
            elif code[it] == "#":
                while code[it] != "\n":
                    l.append((code[it],'comment'))
                    it += 1
                l.append((code[it],'comment'))
            elif code[it] in ' \t\n':
                l.append((code[it],'symbol'))
            else:
                    tmpop = ""
                    tmpkey = ""
                    for kw1 in keywords:
                        # print(code[it])
                        flag = True
                        tmpit2 = it
                        kw = kw1
                        for i in range(len(kw)):
                            if kw[i] != code[tmpit2]:
                                flag = False
                                break
                            tmpit2 += 1
                        if flag:
                            tmpkey = kw
                            break
                    for op in operators:
                        flag = True
                        tmpit = it
                        for i in range(len(op)):
                            if op[i] != code[tmpit]:
                                flag = False
                                break
                            tmpit += 1
                        if flag:
                            tmpop = op
                            break
                    if tmpop == "" and tmpkey == "":
                        l.append((code[it],'unk'))
                    if tmpop != "":
                        l += [(tmpop, "oper")]
                        # print(it,tmpit)
                        it = tmpit - 1
                    if tmpkey != "":
                        l += [(tmpkey, "key")]
                        # print(it,tmpit)
                        it = tmpit2 - 1
                    # print(it)
            it+=1
        except:
            return l
    if flag:
        del l[-1]
    return l
def highlight(t, previousContent):
    content = t.get("1.0", END)
    lines = content.split("\n")
    for tag in t.tag_names():
        t.tag_remove(tag, "1.0", "end")
    if True:
        t.mark_set("range_start", "1.0")
    data = t.get("1.0", "end-1c")
    tmp=syn(data)
    if isinstance(tmp,int):
        tmp=[]
    #print(tmp)
    for content,token in tmp:
        #print(content,token)
        t.mark_set("range_end", "range_start + %dc" % len(content))
        t.tag_add(str(token), "range_start", "range_end")
        t.mark_set("range_start", "range_end")

def temp():
    if platform.system()=='Windows':
        return os.environ['TMP']
    else:
        return '/tmp'

def setcolor(t):
    with open('syncfg.json','r',encoding='utf-8') as f:
        js=load(f)
    for i in js.keys():
        if i=='bg':
            t.configure(background=js[i])
        else:
            t.tag_configure(i,foreground=js[i])
wn = Tk()
wn.geometry(f"500x500")
#wn.attributes("-fullscreen",True)
wn.title("FPDev FooProg IDE")
sc = Scrollbar(orient=HORIZONTAL)
sc.pack(side=BOTTOM, fill=X)

t = Text(wn, width=500, height=500, wrap=NONE)
t.mark_set("range_start", "1.0")
t.pack(side="top", fill=BOTH, expand=True)
t.config(xscrollcommand=sc.set)
t.configure(font=("Consolas", 16, ""))
sc.config(command=t.xview)
setcolor(t)
ct = t.get("1.0", END)
mn = Menu(wn)
wn.config(menu=mn)
fb = Menu(mn, tearoff=0)
curfile = ""


def openfile():
    global curfile,saved
    fp = tkFileDialog.askopenfilename()
    fp = fp.strip()
    if not fp:
        return
    with open(fp, encoding="ansi",errors='replace') as fo:
        x = fo.read()
    t.delete("1.0", "end")
    t.insert("end", x)
    t.mark_set("insert", "end")
    highlight(t, "")
    curfile = fp
    while curfile in recentfilelist:
        recentfilelist.remove(curfile)
    recentfilelist.append(curfile)
    wn.title('FPDev FooProg IDE - '+curfile)
    saved=True
def openfile1(fp):
    global curfile,saved
    fp = fp.strip()
    if not fp:
        return
    with open(fp, encoding="ansi",errors='replace') as fo:
        x = fo.read()
    t.delete("1.0", "end")
    t.insert("end", x)
    t.mark_set("insert", "end")
    highlight(t, "")
    curfile = fp
    while curfile in recentfilelist:
        recentfilelist.remove(curfile)
    recentfilelist.append(curfile)
    wn.title('FPDev FooProg IDE - '+curfile)
    saved=True

def savefile1():
    global curfile
    x = 1
    while 1:
        if not os.path.exists(os.path.join(os.getcwd(), f"Untitled{x}.fp")):
            with open(f"Untitled{x}.fp", "w", encoding="ansi",errors='replace') as fo:
                fo.write(t.get("1.0", "end"))
            break
        x += 1
    tmb.showinfo("FPDev FooProg IDE", f"Successfully saved code in Untitled{x}.fp")
    curfile = f"Untitled{x}.fp"
    while os.path.abspath(curfile) in recentfilelist:
        recentfilelist.remove(os.path.abspath(curfile))
    recentfilelist.append(os.path.abspath(curfile))
    wn.title('FPDev FooProg IDE - '+curfile)

def change_syn():
    with open('syncfg.json','r',encoding='utf-8') as f:
        js=load(f)
    prp=['Keyword','Number','Binary','Octal','Hexadecimal','Comment','Variable','Unkown character','Symbol','Operator','Background']
    res=['key','number','bin','oct','hex','comment','var','unk','symbol','operator','bg']
    rs=[js[i] for i in res]
    dlg=shdialog(prp,rs)
    with open('syncfg.json','w',encoding='utf-8') as f:
        dct={res[i]:dlg[i] for i in range(len(res))}
        #print(dct)
        dump(dct,f)
    tmb.showinfo('FPDev FooProg IDE','You have to restart FPDev to apply these changes.')
def savefile2():
    global curfile
    with open(curfile, "w", encoding="ansi",errors='replace') as fo:
        fo.write(t.get("1.0", "end"))
    tmb.showinfo("FPDev FooProg IDE", f"Successfully saved code in {curfile}")
    while curfile in recentfilelist:
        recentfilelist.remove(curfile)
    recentfilelist.append(curfile)
    wn.title('FPDev FooProg IDE - '+curfile)

def tictactoe():
    global main
    main.reset()
    main.run()
def savefile():
    global saved
    if wn.title().endswith('[New File]') or wn.title().endswith('IDE'):
        if saveasfile():
            return
    elif curfile:
        savefile2()
    else:
        savefile1()
    saved=True


def newfile():
    global curfile,saved
    if not saved and wn.title()!='FPDev FooProg IDE':
        v=tmb.askyesno('FPdev FooProg IDE','Save the current file?')
        if v:
            savefile()
    t.delete("1.0", "end")
    wn.title('FPDev FooProg IDE - [New File]')
    curfile = ""
    saved=False


def saveasfile():
    global curfile,saved
    fp = tkFileDialog.asksaveasfilename(defaultextension=".fp")
    fp = fp.strip()
    if not fp:
        return True
    with open(fp, "w",errors="replace") as fo:
        fo.write(t.get("1.0", "end"))
    if not fp.endswith(".fp"):
        fp += ".fp"
    tmb.showinfo("FPDev FooProg IDE", f"Successfully saved code in {fp}")
    curfile = fp
    while curfile in recentfilelist:
        recentfilelist.remove(curfile)
    recentfilelist.append(curfile)
    saved=True
    wn.title('FPDev FooProg IDE - '+curfile)
    return False

def viewtokens():
    data=t.get('1.0',END)
    h=tokenize(data)
    if isinstance(h,int):
        showerror('FPDev FooProg IDE','Tokenization failed with return code {}'.format(h))
    token=Tk()
    if platform.system()=='Windows':
        token.iconbitmap(os.path.join(temp(),'temp.ico'))
    txt=Text(token)
    txt.insert('1.0',dumps(h))
    txt.bind('<Key>',lambda d:'break')
    txt.configure(font=("Consolas", 16, ""))
    token.title('Tokens')
    txt.pack()
    token.mainloop()
def run():
    if not saved:
        savefile()
    if not curfile:
        return
    if  not os.path.exists(curfile+'.fb'):
        compile()
    if  not os.path.exists(curfile+'.fb'):
        tmb.showerror('FPDev FooProg IDE','The binary does not exist,maybe the compilation failed')
    if os.stat(curfile+'.fb').st_size > 1000000:
        x=tmb.askyesno('FPDev FooProg IDE','The binary\'s size exceeded 1MB,which will cause the execution result to be undeterminate,are you sure you still want to run?')
        if not x:
            return
    """
    if platform.system()=='Darwin':
        tmb.showerror('Error','Unfortunately,you cannot run FooProg on MacOS,because FooProg interpreter is unavaliable.Please switch to another operating system,or use a virtual machine.')
        return
    """
    term(f"{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'FPPauser')} {os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'fp')} {curfile}.fb")
def compile():
    if not saved and wn.title():
        savefile()
    if not curfile:
        return
    m=Tk()
    m.title('Compilation Window')
    if platform.system()=='Windows':
        m.iconbitmap(os.path.join(temp(),'temp.ico'))
    tx=Text(m,wrap=NONE)
    tx.configure(font=("Consolas", 16, ""))
    tx.bind('<Key>',lambda d:'break')
    bak=sys.stdout
    hooked=PrintHooked(tx)
    sys.stdout=hooked
    with open(curfile,'r',encoding='ansi',errors='replace') as f:
         n=f.read()
    print('Tokenizing...')
    t=time.perf_counter()
    x=tokenize(n)
    if isinstance(x,int):
        print('Tokenization failed with return code %d'%x)
    else:
        print(f'Tokenization ran successfully in {show(time.perf_counter()-t)} secs')
        print('Compiling...')
        t=time.perf_counter()
        bk=tobk(x)
        if isinstance(bk,int):
            print('Compilation failed with return code %d'%x)
        else:
            print(f'Compilation ran successfully in {show(time.perf_counter()-t)} secs')
            with open(curfile+'.fb','wb') as fw:
                fw.write(bk)
            print('Successfully saved compiled program as %s'%(curfile+'.fb'))
    sys.stdout=bak
    del hooked
    tx.pack()
    m.mainloop()
def ds():
    if not saved:
        savefile()
    if not curfile:
        return
    if  not os.path.exists(curfile+'.fb'):
        compile()
    try:
        with open(curfile+'.fb','rb') as f:
            w=f.read()
    except:
        tmb.showerror('FPDev FooProg IDE','The binary does not exist,maybe the compilation failed')
    x=disasm(w)
    tkwin=Tk()
    tkwin.title('Disassembly Window')
    if platform.system()=='Windows':
        tkwin.iconbitmap(os.path.join(temp(),'temp.ico'))
    fw=Text(tkwin,wrap=NONE)
    fw.configure(font=("Consolas", 16, ""))
    fw.bind('<Key>',lambda d:'break')
    if x is not None:
        for  i in x:
            fw.insert('end',' '.join(('\n','%05x'%i[1],'\t',i[0],'\t',w[i[1]:i[2]].hex(' '))))
        fw.pack()
        tkwin.mainloop()
    else:
        tmb.showerror('FPDev FooProg IDE','The binary may be corrupted, so FPDev cannot disassemble it')
def myquit(*a):
    if not saved and wn.title()!='FPDev FooProg IDE':
        v=tmb.askyesno('FPdev FooProg IDE','Save the current file?')
        if v:
            savefile()
    sys.exit()
def cmp():
    t=Thread(target=compile)
    t.start()
def ot():
    if platform.system()=='Windows':
        term(f"{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'FPShell.cmd')} {os.path.dirname(os.path.abspath(sys.argv[0]))} {os.path.dirname(os.path.abspath(curfile))}")
    else:
        term(f"{os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),'FPShell.sh')} {os.path.dirname(os.path.abspath(sys.argv[0]))} {os.path.dirname(os.path.abspath(curfile))}")
def helper():
    warn=''
    """
    if platform.system()=='Darwin':
        warn='\nWARNING:You are using MacOS.Since it\'s almost impossible to compile C++ on MacOS,Some features of FooProg will be unsupported.Please switch to another operating system,or run FPDev on a virtual machine.'
    else:
        warn=''
    """
    tmb.showinfo('About FPDev','FPDev - IDE for FooProg 0.0.1\nThis is the lowest version,so there might be many bugs.'+warn)
fb.add_command(label="New", command=newfile)
fb.add_command(label="Open", command=openfile)
fb.add_command(label="Save", command=savefile)
fb.add_command(label="Save As", command=saveasfile)

pb = Menu(mn, tearoff=0)
pb.add_command(label='Compile',command=compile)
pb.add_command(label="Run", command=run)
pb.add_command(label="View Tokens",command=viewtokens)
pb.add_separator()
pb.add_command(label="Open Terminal",command=ot)
ob=Menu(mn,tearoff=0)
ob.add_command(label='Disassemble',command=ds)
ob.add_command(label='Tic Tac Toe',command=tictactoe)
hb=Menu(mn,tearoff=0)
hb.add_command(label='About FPDev',command=helper)
cb=Menu(mn,tearoff=0)
cb.add_command(label='Syntax Highighter config',command=change_syn)
rf=Menu(mn,tearoff=0)
try:
    with open('recent_files.txt',encoding='utf-8') as f:
        cont=f.readlines()
except:
    rf.add_command(label='You haven\'t opened any files yet!',state=DISABLED)
else:
    number=0
    flag=True
    for i in cont:
        if i.strip():
            rf.add_command(label=f'{number} {i.strip()}',command=lambda x=i.strip():openfile1(x))
            number+=1
            recentfilelist.append(i.strip())
            flag=False
    if flag:
        rf.add_command(label='You haven\'t opened any files yet!',state=DISABLED)
def clear():
    global recentfilelist
    recentfilelist=[]
    tmb.showinfo('FPDev FooProg IDE','You have to restart FPDev to apply these changes.')
fb.add_cascade(label='Recent Files',menu=rf)
fb.add_command(label='Clear Recent Files',command=clear)
fb.add_separator()
fb.add_command(label="Exit", command=myquit)
mn.add_cascade(label="File", menu=fb)
mn.add_cascade(label="Program", menu=pb)
mn.add_cascade(label="Config",menu=cb)
mn.add_cascade(label='Other',menu=ob)
mn.add_cascade(label='Help',menu=hb)
def showPopoutMenu(w, menu):
    def popout(event):
        menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
        w.update()
    w.bind('<Button-3>', popout)
def kb(_):
    global ct,saved
    if not wn.title().startswith('*'):
        wn.title('*'+wn.title())
    saved=False
    highlight(t, ct)
    ct = t.get("1.0", END)
saved=False
wn.bind("<Key>", kb)
wn.protocol('WM_DELETE_WINDOW',myquit)
uuu=b'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'
with open(os.path.join(temp(),'temp.ico'),'wb') as xxx:
    xxx.write(b64decode(uuu))
if platform.system()=='Windows':
    wn.iconbitmap(os.path.join(temp(),'temp.ico'))
menu=Menu(wn)
def aa():
    t.event_generate('<<Copy>>')
def bb():
    t.event_generate('<<Cut>>')
def cc():
    t.event_generate('<<Paste>>')
def term(x):
    if platform.system()=='Windows':
        from subprocess import run
        run('cmd /c start '+x,shell=False)
    elif platform.system()=='Linux':
        os.system('gnome-terminal --command \''+x+'\'')
    else:
        os.system(f'osascript -e \'tell application \"Terminal\" to do script \'{x}\'\'')
menu.add_command(label='Copy',command=aa)
menu.add_command(label='Cut',command=bb)
menu.add_command(label='Paste',command=cc)
showPopoutMenu(t,menu)
if len(sys.argv)>1:
    try:
        with open(sys.argv[1],'r',encoding='ansi',errors='replace') as f:
            x=f.read()
    except:
        wnd=Tk()
        wnd.withdraw()
        wn.destroy()
        tmb.showerror('FPDev FooProg IDE','The file you try to open doesn\'t exist.')
        wnd.mainloop()
        sys.exit(-1)
    t.insert('end',x)
    highlight(t, ct)
    ct = t.get("1.0", END)
    curfile=sys.argv[1]
    wn.title('FPDev FooProg IDE - '+curfile)

try:
    wn.mainloop()
except BaseException as e:
    if not isinstance(e,SystemExit):
        tmb.showerror('The FPDev FooProg IDE has crashed',f'Error is {e}')
with open('recent_files.txt','w',encoding='utf-8') as f:
    for i in recentfilelist:
        f.write(i+'\n')