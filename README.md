IsatPhonePro GMR-2 plaintext/ciphertext/cipherstream
====================================================
Firmware v4.0.0

WARNING
=======

This is very experimental code and some garbage appears to have been intermixed with some blocks. Specifically plaintext.bin and ciphertext.bin should not contain any value other than 0x0000 and 0x0001 but sometimes garbage gets in.
Also, the dumper functions are primitive and if too many packets are encrypted the dumper will start to drop packets. In fact this happens often, you should not regard the dumps as a continous stream.


Description:
------------
Dump of ciphered and plain data


Directories:
------------

 * balance-enquiry1 : dump of two complete "balance enquiry" operations (USSD requests)
 * balance-enquiry2 : dump of two complete "balance enquiry" operations (USSD requests)
 * bin : Binaries and scripts used
 * src : Sources


Every dump was done immediately after the phone boot-up.

The dumps were made by copying buffers from the applycipher() function (See applycipher.jpg) before and after combination of the plaintext with the ciphertext.

By looking at the applycipher() function it is clear that the R0 register is a pointer to the input/ouput buffer and the R1 register is a pointer to the cipher stream.



Generation of the dumps:
------------------------
The steps to generate the dumps are:
 * ISATPhonePro terminal to the computer via USB
 * Execute bin/dopatch_out.sh to do the memory-patching
 * Execute dump_out_packets.py to stablish a serial communication to the satellite terminal and dump the buffers


File format of the dumps:
-------------------------
Each dump contains three files:
 * cipherstream.bin
 * ciphertext.bin
 * plaintext.bin

Both plaintext.bin and ciphertext.bin consist in N blocks of 256 bytes, each one containing 120 bits of user data (encoded as one bit for every word).
cipherstream.bin consist in N blocks of 16 bytes, each one containing 128 bits of cipherstream.
Diagram:
```
plaintext.bin:     [ block 1 (256 bytes)][ block 2 (256 bytes)], etc.
ciphertext.bin:    [ block 1 (256 bytes)][ block 2 (256 bytes)], etc.
cipherstream.bin:  [ block 1 (16 bytes )][ block 2 (16 bytes )], etc.
```

The encryption algorithm used to combine each block of plaintext.bin and cipherstream.bin into a block of ciphertext.bin is located in the function applycipher().


![applycipher graph](/applycipher.png "applycipher code graph")

