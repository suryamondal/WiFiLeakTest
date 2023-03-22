#!/usr/bin/python

###############################################
# Oct 23, 2018 : Suryanarayan Mondal
#
###############################################

import sys

DATAFILEBASEDIR = "../data"

index_datafile = "%s/RPC_Names" % (DATAFILEBASEDIR)
index_ofile = open(index_datafile,'a')
index_ofile.close()

stations = []
names = []
runs = []
errors = []
line_cnt = 0

with open(index_datafile,'r') as f:
    for line in f:
        lines = line.rstrip('\n')
        c,a,b,d = lines.split()
        stations.append(c)
        names.append(a)
        runs.append(b)
        errors.append(d)
        line_cnt += 1
        
# print line_cnt,stations,names,runs,errors

select = input("O to Enter RPC Name\n1 to Reset RPC Name\n3 to See RPCs: ")

if select == 3:
    print ""
    if int(line_cnt)==0:
        print "No Data\n"
        sys.exit()
    for ij in range(0,int(line_cnt)):
        print "Station: %s\tRPC: %s\tRunNo: %s\tOffset: %s" % (stations[ij],names[ij],runs[ij],errors[ij])
    print ""
    sys.exit()

station = raw_input("Enter Station No (1-15): ")

r_stations = []
r_names = []
r_runs = []
r_errors = []

t_cnt = line_cnt
line_cnt = 0
for ij in range(0,int(t_cnt)):
    # print ij, stations[ij]
    if int(stations[ij])!=int(station):
        # print ij,int(stations[ij]),int(station)
        r_stations.append(stations[ij])
        r_names.append(names[ij])
        r_runs.append(runs[ij])
        r_errors.append(errors[ij])
        line_cnt += 1

# print r_stations,r_names,r_runs,r_errors

if int(select) == 0:
    rpc_name = raw_input("Enter Full RPC Name: ")
    run_no = raw_input("Enter Run No: ")
    error = raw_input("Enter Error at Station: ")
    isPresent = -100
    for ij in range(0,int(line_cnt)):
        if r_names[ij]==rpc_name:
            if int(isPresent)!=-100:
                print ""
                print "**********************************"
                print "Same RPC is present more than once"
                print "Rectify the file ../data/RPC_Names"
                print "**********************************"
                print ""
                sys.exit()
            isPresent = ij
    if int(isPresent)==-100:
        r_stations.append(station)
        r_names.append(rpc_name)
        r_runs.append(run_no)
        r_errors.append(error)
        line_cnt += 1
    else:
        r_stations[int(isPresent)] = station
        r_names[int(isPresent)] = rpc_name
        r_runs[int(isPresent)] = run_no
        r_errors[int(isPresent)] = error
        
# print line_cnt,stations,names,runs,errors
    
index_ofile = open(index_datafile,'w')

for ij in range(0,int(line_cnt)):
    outdata = "%s %s %s %s\n" % (r_stations[ij],r_names[ij],r_runs[ij],r_errors[ij])
    # print ij,outdata
    # print stations[ij],names[ij],runs[ij],errors[ij]
    index_ofile.write(outdata)

index_ofile.close()
