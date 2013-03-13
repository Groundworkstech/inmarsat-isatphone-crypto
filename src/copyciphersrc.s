# This function is designed to be called from inside the apply_cipher function to copy a packet about to be sent
# Will copy the src data and the cipher stream
# can be placed anywhere. Ex.:
# ./isat_hax_echo_bf.py ./blackfin_sdk/copyout.bin 0x20180000

.section .rodata
 
 
.text
.align 4
 
.global _main;
.type _main, STT_FUNC;

.equ    PACKETLEN,0x100 # shoud be enough for max. 240 bits frame
.ascii "STRT" ;

_main:
	/* Blackfin requires at least 12 bytes when calling functions */
	LINK 0x0c
	[--SP] = ASTAT;
	[--SP] = RETS;
	[--SP] = (R7:0);
	[--SP] = (P5:0);

	#P5=R0 # R0=SRC stream
	#P4=R1 # R0=CRYPT stream

	P0.L=0x1000
	P0.H=0x208A # 0x208A1000:
	

	R0=B[P0](Z)
	R0+=1
	R1=0x100
	CC = R0 < R1
	if CC JUMP noover
	# overflow
	R0=0
noover:
	B[P0]=R0;

	############ Copy SRC buf

	R1.L=0x2000
	R1.H=0x208A # 0x208A2000: 
	P1=R1 #I0=dst pointer

	// Dump position
	P0=P5 #P0=src pointer

	R1=PACKETLEN #R1=count
loop1:
	R0=B[P0++] (Z)
	B[P1++]=R0
	R1+=-1
	CC=R1==0
	if !CC JUMP loop1

	############ Copy Crypt buf
	R1.L=0x2200
	R1.H=0x208A # 0x208A2200: 
	P1=R1 #P1=dst pointer

	// Dump position
	P0=P4 #P0=src pointer

	R1=PACKETLEN #R1=count
loop2:
	R0=B[P0++] (Z)
	B[P1++]=R0
	R1+=-1
	CC=R1==0
	if !CC JUMP loop2

end:
	(P5:0) = [SP++]; // Restore registers from Stack
	(R7:0) = [SP++];
	RETS = [SP++];
	ASTAT = [SP++];
	UNLINK
	R7 = 0x1 (X); # ran out of space in hook, overwrote this instruction (correspond to 0x20686582)
	RTS;
.align 4
pad_string: .string   "AAAA"
end_string: .string   "THEEND"
.size _main,.-_main;
