# File Structure Exploitation 

This python module is for generating payloads to exploit the FILE structure in C. Can be used in CTF challenges.

## Usage

**FileStructure(arch, null)** - returns an object that can stimulate the FILE structure in C

1. arch - specify the architecture. It can be -
    * 64 - amd64
    * 32 - i386
2. null - an address pointing to null value

**write(addr,size)** - function in FileStructure. Returns payload for writing data from arbitrary address to stdout. Arguments are-

1. addr - the address from where the data is to be written out
2. size - the size of data to be written

**read(addr,size)** - function in FileStructure. Returns payload for reading data to arbitrary address from stdin. Arguments are-
       
1. addr - the address where the data is to be read
2. size - she size of data to be read


## Examples 

See PoC

## Credits

Angelboy (@scwuaptx) and his slide's on File Structures - <a href="http://4ngelboy.blogspot.in/2017/11/play-with-file-structure-yet-another.html">Play with FILE Structure</a>
