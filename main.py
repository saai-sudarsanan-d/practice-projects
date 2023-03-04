import tkinter as tk
from scanner import scanner
from multiprocessing import Process
import os

window = tk.Tk()
window.title("Scanner")
window.rowconfigure([0,1,2,3,4],minsize=50)
window.columnconfigure([0,1,3],minsize=50)

global plist
plist = []

def Scan(sig):
    if sig == 1:
        target = str(targetEntry.get())
        start = int(startPort.get())
        try:
            end = int(endPort.get())
        except:
            end = start
        p = Process(target=scanner,args=(target,start,end))
        plist.append(p)
        p.start()
    if sig == 0:
        print("Killing all Processes...")
        for p in plist:
            p.kill()
        print("Done")
        os.system("clear")

label1 = tk.Label(text="Enter Target Name/IP: ")
targetEntry = tk.Entry()
label2 = tk.Label(text="Enter Start Port: ")
startPort = tk.Entry()
label3 = tk.Label(text="Enter End Port (Optional): ")
endPort = tk.Entry()
label4 = tk.Label(text="Kill Process: ")
killprocess = tk.Entry()

start = tk.Button(text="Start Scan",command=lambda:Scan(1))
# stop = tk.Button(text="Stop Scan",command=lambda:Scan(0))
killall = tk.Button(text="Kill All",command=lambda:Scan(0))

label1.grid(row=0,column=0)
targetEntry.grid(row=0,column=1)
label2.grid(row=1,column=0)
startPort.grid(row=1,column=1)
label3.grid(row=2,column=0)
endPort.grid(row=2,column=1)

start.grid(row=3,column=0)
# stop.grid(row=3,column=1)
# label4.grid(row=4,column=0)
# killprocess.grid(row=4,column=1)
killall.grid(row=3,column=2)

window.mainloop()