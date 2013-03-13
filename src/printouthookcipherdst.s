# This function is designed to be embedded inside the ApplyCipher function to hook the printlog.s code
# Ex.: /isat_hax_echo_bf.py ./bfpatch/printouthook.bin 0x206865B0

.section .rodata
 
 
.text
.align 4
 
.global _main;
.type _main, STT_FUNC;

.ascii "STRT" ;

_main:
	NOP
	P0.L=0x0800
	P0.H=0x2018 # puts
	call (P0);
	SP += 0xc;
	(R7:4,P5:4) = [SP++];
	UNLINK;
	R0 = 0x0;	
	RTS;
	NOP;
.align 4
end_string: .string   "THEEND"
.size _main,.-_main;
