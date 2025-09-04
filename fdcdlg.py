from tkinter import *
import tkinter.messagebox as tmb
import platform,os
def temp():
    if platform.system()=='Windows':
        return os.environ['TMP']
    else:
        return '/tmp'
def ishtc(x):
    if len(x)!=7:
        return False
    for i in range(1,6):
        if(x[i] not in '0123456789ABCDEF'):
            return False
    return True
def shdialog(prompts,choice):
    result=[]
    wn=Tk()
    if platform.system()=='Windows':
        wn.iconbitmap(os.path.join(temp(),'temp.ico'))
    #print(id(wn))
    wn.title('Syntax Highlighting')
    wn.geometry(f'200x{60*len(prompts)+60}')
    def fun(res):
        for j in entrys:
            if not ishtc(j.get()):
                tmb.showerror('Error','The color is not a valid HTML color')
                return
        res.append([j.get() for j in entrys])
        #print(id(wn))
        wn.quit()
        wn.destroy()
    btn=Button(wn,text='Apply',command=lambda r=result:fun(r))
    btn.place(y=60*len(prompts),x=10,width=80,height=20)
    labels=[]
    entrys=[]
    for i in range(len(prompts)):
        labels.append(Label(wn,text=prompts[i]))
        labels[-1].place(y=10+i*50,x=10,width=80,height=40)
        entrys.append(Entry(wn))
        entrys[-1].insert(END,choice[i])
        entrys[-1].place(y=10+i*50,x=100,width=80,height=40)
    wn.mainloop()
    #print(result)
    return result[0]
#print(shdialog('114514','123456'))