#!/usr/bin/python

import sys
import os
import time
import Tkinter as tk


DATAFILEBASEDIR = "../data"

stations = sys.argv[1:]

if stations[0]=="":
    sys.exit()

index_datafile = "%s/RPC_Names" % (DATAFILEBASEDIR)

names = ""
runs = ""

with open(index_datafile,'r') as f:
    for line in f:
        lines = line.rstrip('\n')
        c,a,b,d = lines.split()
        if int(stations[0])==int(c):
            names = a
            runs = b

outdataFile = "%s/%s_%s_lt.dat" % (DATAFILEBASEDIR,names,runs)
cmdTime = "tail -n 1 %s | awk '{print $1}'" %(outdataFile)
cmdPD = "tail -n 1 %s | awk '{print $5-$3}'" %(outdataFile)

counter = 0
def counter_label(label):
    def count():
        global counter
        counter = "%s\n%s" % (time.strftime('%H:%M:%S', time.localtime(int(os.popen(cmdTime).read()))),os.popen(cmdPD).read())
        label.config(text=str(counter).rstrip())
        label.after(2000, count)
    count()

if runs!="":
    rootName = "RPC# " + names + "    Run# " + runs
    root = tk.Tk()
    root.title(str(rootName).rstrip())
    label = tk.Label(root, font=('Times', '150'),fg='red')
    label.pack(expand=True)
    counter_label(label)
    button = tk.Button(root,text='Close',command=root.destroy)
    button.pack()
    root.mainloop()
