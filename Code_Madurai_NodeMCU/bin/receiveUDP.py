#!/usr/bin/python

###############################################
# Oct 23, 2018 : Suryanarayan Mondal
# suryamondal@gmail.com
###############################################


import time
import datetime
import os
import sys
import commands
from ctypes import c_short
# from math import pow
import socket

DATAFILEBASEDIR = "../data"

maxRPC = 100

UDP_PORT = 5006
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

r_temperature = -100
r_pressure = -100

time_now = int(time.time())
atm_datafile = "%s/%s_atm.dat" % (DATAFILEBASEDIR,time_now)

data_atm_cnt = 0                # 25000 lines in each atm data file
printdata = ""
printrpcdata = ""
lastRefTime = -100;
lastModTime = -100;

rpc_cnt = 0
names = []
runs = []
errors = []
fileTime = [0] * maxRPC

while True:

    time_now = int(time.time())
    
    index_datafile = "%s/RPC_Names" % (DATAFILEBASEDIR)
    t_lastModTime = os.path.getmtime(index_datafile)
    
    if int(t_lastModTime)!=int(lastModTime):
        # print time_now
        time.sleep(2);
        # print time_now
        rpc_cnt = 0
        names = [-100] * maxRPC
        runs = [0] * maxRPC
        errors = [0] * maxRPC
        with open(index_datafile,'r') as f:
            for line in f:
                lines = line.rstrip('\n')
                c,a,b,d = lines.split()
                # names.append(a)
                # runs.append(b)
                # errors.append(d)
                if int(c)<int(maxRPC):
                    names[int(c)] = a
                    runs[int(c)] = b
                    errors[int(c)] = d
                    rpc_cnt += 1
                
    # print rpc_cnt
    # print names
    lastModTime = t_lastModTime
    # print lastModTime
    
    data,addr = sock.recvfrom(1024)
    # print "received message:", data
    # print "received addr:", addr
    
    station,temperature,pressure = data.split();
    # print station,temperature,pressure
    
    if int(station)==0:
        r_temperature = temperature
        r_pressure = pressure
        # print r_temperature,r_pressure
        
        printdata = "%s %2.2f %5.1f " % (time_now,float(temperature),float(pressure))        
        atm_ofile = open(atm_datafile,"a")
        atm_ofile.write(printdata)
        atm_ofile.write("\n")
        atm_ofile.close()
        
        # print printdata
        
        data_atm_cnt += 1
        lastRefTime = time_now
        
    if str(names[int(station)])!="-100" and int(lastRefTime)>0 and int(time_now)-int(lastRefTime)<15 and int(rpc_cnt)>0 and int(station)>0 and int(station)<int(maxRPC) and fileTime[int(station)]!=int(lastRefTime):
        printrpcdata = printdata
        printrpcdata += "%2.2f %5.1f" % (float(temperature),float(pressure) - int(errors[int(station)]))
        # print printrpcdata
        printrpcdata += "\n"
        rpc_datafile = "%s/%s_%i_lt.dat" % (DATAFILEBASEDIR,names[int(station)],int(runs[int(station)]))
        rpc_ofile = open(rpc_datafile,"a")
        rpc_ofile.write(printrpcdata)
        rpc_ofile.close()
        fileTime[int(station)]=lastRefTime
        
    if int(data_atm_cnt) == 25000:
        atm_datafile = "%s/%s_atm.dat" % (DATAFILEBASEDIR,time_now)
        data_atm_cnt = 0
        
    # print fileTime
    
if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
    sys.exit()
