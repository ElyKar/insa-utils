#!/usr/bin/python

import subprocess, sys, re


# Top-level elements

def fill (n) :
    if n < 0:
        return ""
    i = 0
    res = ""
    while i < n:
        res += " "
        i += 1
    return res

# Request all educational computers registered on CS department range (10.131.42.0/24)
dig = subprocess.Popen(""" dig @10.4.1.79 axfr educ.insa | grep "10.131.42" """, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = dig.communicate()
errcode = dig.returncode

if errcode != 0:
    print("Error, dig exited with status: " + str(errcode) + "\n" + err)
    sys.exit(0)

hosts = re.findall(r"\w+\.educ\.insa", out)

up = 0
uplist = []
down = 0

tab = 27

print "\t+------------------------------+-------+"

for hostname in hosts :
    ping = subprocess.Popen("ping -c 1 -w 1 " + hostname, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = ping.communicate()
    response = ping.returncode
    if response == 0:
        up += 1
        print "\t|\033[92m", hostname, fill(tab-len(hostname)), "\033[0m|is up  |"
    	print "\t+------------------------------+-------+"
        uplist += [hostname]
    else:
        down += 1

print "up ->", up, "down ->", down

b = ""
while b != "n" and b != "y" and b != "a":
    b = raw_input("Do you want to connect to a pc?[y/n/a] ")

if b == "y":
 s   usr = raw_input("username? ")
    os.system("ssh "+usr+"@"+uplist[0])

elif b == "a":
    pc = ""
    ok = False
    while not ok :
        pc= raw_input("PC name? ")
        if uplist.count(pc+".educ.insa") != 1 :
            print "Unavailable."
        else :
            ok = True
    usr = raw_input("username? ")
    os.system("ssh "+usr+"@"+pc+".educ.insa")

print "bye"
