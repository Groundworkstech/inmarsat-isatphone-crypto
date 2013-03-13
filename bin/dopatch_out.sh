######
###### Series of patches to enable dumping of output packet on the IsatPhonePRO firmware
######


# Install ARM patcher
./isat_hax_echo_arm.py ./isat_blackfin_patcher.bin

##### Write patches
# Install Packet copier (src and ciph stream)
./isat_hax_echo_bf.py ./copyciphersrc.bin 0x20180000

# Install Packet copier (dst)
./isat_hax_echo_bf.py ./copycipherdst.bin 0x20180800

# hook ApplyCipher_2068656E  (pre-cipher)
./isat_hax_echo_bf.py ./printouthook.bin 0x20686578

# hook ApplyCipher_2068656E  (post cipher)
./isat_hax_echo_bf.py ./printouthookcipherdst.bin 0x206865B0

# Install echo-peek command
./isat_hax.py ISATPeek-nice.bin
