# This function is designed to be embedded inside the ApplyCipher function to hook the printlog.s code
# Ex.: /isat_hax_echo_bf.py ./bfpatch/printouthook.bin 0x20686578

.section .rodata
 
 
.text
.align 4
 
.global _main;
.type _main, STT_FUNC;

.ascii "STRT" ;

_main:
	P0.L=0x0000
	P0.H=0x2018 # puts
	call (P0);
	SP+= -0xc;

.align 4
end_string: .string   "THEEND"
.size _main,.-_main;
