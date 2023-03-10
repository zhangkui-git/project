import time
import tkinter
import tkinter as tk
import tkinter.messagebox
import socket
import threading
import sys

lock_data = threading.RLock()

"""
ip, port, flow, count, time
"""


def putUdp():
    a, b, c, d, e = show()
    arg1 = a
    arg2 = int(b)
    arg3 = c
    arg4 = int(d)
    arg5 = float(e)
    n = 1

    try:
        while n <= arg4:
            conn = socket.socket(type=socket.SOCK_DGRAM)
            ip = arg1
            port = arg2
            lock_data.acquire()
            conn.sendto(arg3.encode("utf-8"), (ip, port))
            lock_data.release()
            conn.close()
            n += 1
            time.sleep(arg5)
        tkinter.messagebox.showinfo(message=f'{arg4}条Udp包发送成功')
    except:
        tkinter.messagebox.showwarning(message='Udp包发送失败')



def putTcp():
    a, b, c, d, e = show()
    arg1 = a
    arg2 = int(b)
    arg3 = c
    arg4 = int(d)
    arg5 = float(e)
    n = 1
    try:
        while n <= arg4:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 绑定端口，发送数据时会从绑定的端口发送，不会再生成随机端口
            # tcp_socket.bind(("*.*.*.*", 8001))
            tcp_socket.connect((f'{arg1}', arg2))
            tcp_socket.send(arg3.encode("utf-8"))
            tcp_socket.close()
            n += 1
            time.sleep(arg5)
        tkinter.messagebox.showinfo(message=f'{arg4}条Tcp包发送成功')
    except:
        tkinter.messagebox.showwarning(message='Tcp包发送失败')




def inputclear():
    var1.set('')
    var2.set('')
    var3.set('')
    var4.set('')
    var5.set('')


def show():
    output1 = var1.get().strip()
    output2 = var2.get().strip()
    output3 = var3.get().strip()
    output4 = var4.get().strip()
    output5 = var5.get().strip()
    return output1, output2, output3, output4, output5


top = tk.Tk(className='tcp&udp_PutFlow')
top.geometry('1000x600+100+100')

var1 = tkinter.StringVar()
var2 = tkinter.StringVar()
var3 = tkinter.StringVar()
var4 = tkinter.StringVar()
var5 = tkinter.StringVar()

l1 = tkinter.Label(top, text="目的IP:")
l1.config(font=("Arial", 20))
l1.place(x=300, y=80)
# l1.pack()
# var1.set('请输入整数')
e1 = tkinter.Entry(top, textvariable=var1, bd=5)
e1.pack()
e1.place(width=300, height=40, x=430, y=80)
# e1.pack()

l2 = tkinter.Label(top, text="目的端口:")
l2.config(font=("Arial", 20))
l2.place(x=300, y=140)
# l2.pack()
# var2.set('请输入整数')
e2 = tkinter.Entry(top, textvariable=var2, bd=5)
e2.pack()
e2.place(width=300, height=40, x=430, y=140)
# e2.pack()

l4 = tkinter.Label(top, text="触发次数:")
l4.config(font=("Arial", 20))
l4.place(x=300, y=200)
# l2.pack()
# var2.set('请输入整数')
e4 = tkinter.Entry(top, textvariable=var4, bd=5)
e4.pack()
e4.place(width=300, height=40, x=430, y=200)
# e2.pack()


l3 = tkinter.Label(top, text="信息流:")
l3.config(font=("Arial", 20))
l3.place(x=300, y=320)
# l2.pack()
# var2.set('请输入整数')
e3 = tkinter.Entry(top, textvariable=var3, bd=5)
e3.pack()
textwrap = "none"
e3.place(width=500, height=140, x=430, y=320)
# e2.pack()

l5 = tkinter.Label(top, text="时间间隔:")
l5.config(font=("Arial", 20))
l5.place(x=300, y=260)
# l2.pack()
# var2.set('请输入整数')
e5 = tkinter.Entry(top, textvariable=var5, bd=5)
e5.pack()
e5.place(width=300, height=40, x=430, y=260)
# e2.pack()


# top_down = tkinter.Label(top, text='(注：只能输入整数，计算方式：第二个数字 - 第一个数字)')
# top_down.place(x=80, y=190)

com1 = tkinter.Button(top, text='Tcp',  command=putTcp)
com1.configure(font=("Arial", 15))
com1.place(x=240, y=400, )
com2 = tkinter.Button(top, text='Udp', command=putUdp)
com2.configure(font=("Arial", 15))
com2.place(x=500, y=400)
# com3 = tkinter.Button(top, text='暂停', command=stop)
# com3.configure(font=("Arial", 15))
# com3.place(x=600, y=400)
com4 = tkinter.Button(top, text='重置', command=inputclear)
com4.configure(font=("Arial", 15))
com4.place(x=760, y=400)

top_down = tkinter.Label(top, text='注：端口，次数只能为正整数 && 间隔只能为正数(例如：1 或 0.5)', font=("Arial", 15), fg='Crimson')
# top_down.config(font=("Arial", 15))
top_down.place(x=240, y=500)


top.mainloop()



