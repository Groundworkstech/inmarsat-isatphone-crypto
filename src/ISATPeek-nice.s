@ Shellcode that prints $PC
@ Usage:
@   python isat_hax.py ./ISATHello.bin

.thumb

.ascii "STRT"  @ START MARK

@+1 because blx+1 is a jump to Thumb code
.equ 	HANDLE,0x214784e8 @UART Handle (see processing of AT commands @ 0x004e3f6ec)
.equ 	PUTS,0x04E8C7E4+1 @PUTS(handle,char *str,int size) function inside firmware
.equ    SPRINTF,0x04EB0960+1 @int SPRINTF(char *buf,char *str,...) function inside firmware

.equ    DUMPAREA, 0x2148BB28 @ Memory dump area

.equ 	get_input_param, 0x04e98500+1
.equ 	atoi, 0x04e9a3fc+1
	push {R1-R7,LR}


	#bl FDUMPAREA
	mov r0,r0
	ldr r7,=get_input_param
	blx r7
	@now in r0 is the first param

	@convert param
	mov r0,r0 @ string
	mov r1,#0	@ ??
	mov r2,#0x10 @base
	ldr r7,=atoi
	blx r7

	@print
	@mov r1,r0
	@adr r0,frmt1
	@bl PRINTF

	bl FDUMPAREA

	@return
	mov r0,#0
	pop {R1-R7,PC}

FDUMPAREA: @R0=memory position to dmp

	push {r0-r7,LR}

	mov r2,r0
	mov r6, #16
loop1:
	adr r0,frmt1
	mov r1,r2
	bl PRINTF

	mov r7, #16
loop2:
	mov r1,#0
	ldrB r1,[r2]
	adr r0,frmt2
	bl PRINTF
	add r2,#1
	sub r7,#1
	cmp r7,#0
	bne loop2
	sub r6,#1
	cmp r6,#0
	bne loop1

	pop {r0-r7,PC}

PRINTF: @R0=format R1,R2,R3,R4=vars
	push {r0-r7,LR}

	@ adjust regs for sprintf
	push {r0-r4}
	pop {r1-r5}	

	@ call sprintf
	add R0,PC,#1000 @dst buf
	push {r0}
	ldr R7,=SPRINTF
	blx R7

	@ call puts
	mov r2,r0
	pop {r1}
	ldr r0,=HANDLE
	add R0,#0xFF
	add R0,#0x65
	ldr r7,=PUTS
	blx r7

	pop {r0-r7,PC}

	

.align 4
crlf: .asciz "\n"
.align 4
frmt1:	.asciz "\n0x%08X: "
.align 4
frmt2:	.asciz "%02X "

