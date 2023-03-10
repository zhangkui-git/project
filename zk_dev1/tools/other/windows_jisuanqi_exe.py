import tkinter
import tkinter as tk
import tkinter.messagebox


def f2():
    arg1, arg2 = show()
    try:
        res = int(arg2) - int(arg1)
        tkinter.messagebox.showinfo(message=f'计算结果是：{res}')
    except:
        tkinter.messagebox.showwarning(message='请检查两个数字是否都是整数')


def f1():
    arg1, arg2 = show()
    try:
        res = int(arg2) + int(arg1)
        tkinter.messagebox.showinfo(message=f'计算结果是：{res}')
    except:
        tkinter.messagebox.showwarning(message='请检查两个数字是否都是整数')


def f3():
    arg1, arg2 = show()
    try:
        res = int(arg2) * int(arg1)
        tkinter.messagebox.showinfo(message=f'计算结果是：{res}')
    except:
        tkinter.messagebox.showwarning(message='请检查两个数字是否都是整数')


def f4():
    arg1, arg2 = show()
    try:
        res = int(arg2) / int(arg1)
        tkinter.messagebox.showinfo(message=f'计算结果是：{res}')
    except:
        tkinter.messagebox.showwarning(message='请检查两个数字是否都是整数')


def inputclear():
    var1.set('')
    var2.set('')


def show():
    output1 = var1.get().strip()
    output2 = var2.get().strip()
    return output1, output2


top = tk.Tk(className='张奎爱妻王灿专属计算器')
# top.title('京城三"骚"专属之差计算器')
top.geometry('500x400+100+100')

var1 = tkinter.StringVar()
var2 = tkinter.StringVar()

l1 = tkinter.Label(top, text="第一个数字:")
l1.place(x=100, y=40)
# l1.pack()
# var1.set('请输入整数')
e1 = tkinter.Entry(top, textvariable=var1, bd=5)
e1.pack()
e1.place(x=170, y=40)
# e1.pack()

l2 = tkinter.Label(top, text="第二个数字:")
l2.place(x=100, y=80)
# l2.pack()
# var2.set('请输入整数')
e2 = tkinter.Entry(top, textvariable=var2, bd=5)
e2.pack()
e2.place(x=170, y=80)
# e2.pack()

top_down = tkinter.Label(top, text='(注：只能输入整数，计算方式：第二个数字 - 第一个数字)')
top_down.place(x=80, y=190)

com1 = tkinter.Button(top, text='加法', command=f1)
com1.place(x=80, y=140)
com2 = tkinter.Button(top, text='减法', command=f2)
com2.place(x=150, y=140)
com3 = tkinter.Button(top, text='乘法', command=f3)
com3.place(x=220, y=140)
com4 = tkinter.Button(top, text='除法', command=f4)
com4.place(x=290, y=140)
new_com = tkinter.Button(top, text='重置', command=inputclear)
new_com.place(x=360, y=140)

top.mainloop()



