#!/usr/bin/python
import sys,struct,os

from serial import *
import time,math

# serial object
# please adjust to device properties
serial = Serial(port="/dev/ttyACM0",baudrate=9600,bytesize=EIGHTBITS,parity=PARITY_NONE,stopbits=STOPBITS_ONE,timeout=None,xonxoff=0,rtscts=0)


#Send command via serial
def send(str):
	ret=""
	serial.write(str)
	for i in range(100):
		time.sleep(0.02)
		if serial.inWaiting()==0:
			break
		ret+= serial.read(serial.inWaiting())
	return ret

def send_cmd(str):
	recv_data = send("\r\nat@xsh=\"%s\"\r\n" % str)
	recv_data = recv_data.replace("\r\n\r\n", "")	
	return recv_data

#return single bit from string
def getbit(buf,bitnum):
	bitpos = bitnum % 8
	bytepos=math.floor(bitnum/8)
	byte = buf[int(bytepos)]
	if (ord(byte) & (1<<bitpos)) != 0:
		return True
	else:	return False

def getbits(buf,start,end):
	end+=1
	val=0
	cnt=0
	str=""
	for i in range(start,end):
		if getbit(buf,i):
			val+=1<<cnt
		if (cnt!=0):
			if (cnt % 7)==0:
				str+=chr(val)
				val=0
				cnt=-1
		cnt+=1
	if cnt!=0:
		str+=chr(val)
	return str

def printHexLine(line):
	stri=""
	for c in line:
		stri+=" %02X " % ord(c)
	stri+="|"
	for c in line:
		echar=ord(c)
		if (echar<32) or (echar>128): echar=ord('.')
		stri+="%c" % echar
	return stri

		

# print blackfin memory address. Optionally return string with data
def printAddr(addr,show=0):
	data=""
	recv_data = send_cmd("echo %08X" % addr)
	recv_data=recv_data.split()	
	#print recv_data
	for i in range(0x10):
		str=recv_data[i*0x11]
		for c in range(0x10):
			str+=" %s" % recv_data[i*0x11+c+1]
		str+="|"
		for c in range(0x10):
			echar = int(recv_data[i*0x11+c+1],16);
			data+="%c" % echar
			if (echar<32) or (echar>128): echar=ord('.')
			str+="%c" % echar
		if show==1:
			print str
	return data

##Main
oldpackets=99
os.system("rm dumped_packets.bin;touch dumped_packets.bin")
os.system("rm dumped_cipher_stream.bin;touch dumped_cipher_stream.bin")
skipped=0
while(True):
		recv_data = send_cmd("echo %08X" % 0x208A1000) # counter
		recv_data=recv_data.split()
		try:
			packets=int(recv_data[1],16)
			if (packets!=oldpackets):
				skipped = packets-oldpackets
				oldpackets=packets
				os.system("clear")
				print "packets: %d skipped packets: %d" % (packets,skipped)
				src = printAddr(0x208A2000,1) # src buff
				print len(src)
				stri=""
				for i in range(10):
					num=0
					line=""
					for c in range(6):
						line+="%d" % ord(src [ ((i*24)+(c*4)) ] )
						num+=ord(src[ ((i*24)+(c*4)) ])<<c
					print "--- %d: %s" % (i,line)
					if (num>0xff): num=0xff
					stri+=chr(num)
				ciph = printAddr(0x208A2200) # cipher stream
				dst = printAddr(0x208A2400) # dst buff

				print (" SRC data: %s " % printHexLine(stri))
				print ("CYPH strm: %s " % printHexLine(ciph[0:15]))

				#sys.stdout.flush()
				a=open("plaintext.bin","ab")
				a.write(src)
				a.close()

				a=open("cipherstream.bin","ab")
				a.write(ciph[:0x10])
				a.close()

				a=open("ciphertext.bin","ab")
				a.write(dst)
				a.close()


		except: pass

