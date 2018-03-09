<b>File Structure Exploitation</b>
---------------------------

This python module is for generating payloads to exploit the FILE structure in C. Can be used in CTF challenges.

<b>Usage</b>
-----

FileStructure(arch, null) - returns an object that can stimulate the FILE structure in C<br />
                            <ul>
                              <li> arch - specify the architecture. It can be -
                                <ul>
                                  <li> 64 - amd64
                                  <li> 32 - i386
                                </ul>
                              <li> null - an address pointing to null value
                             </ul>

write(addr,size) - function in FileStructure. Returns payload for writing data from arbitrary address to stdout. Arguments are-<br /> 
                        <ul>  
                          <li> addr - the address from where the data is to be written out
                          <li> size - the size of data to be written
                         </ul>

read(addr,size) - function in FileStructure. Returns payload for reading data to arbitrary address from stdin. Arguments are -<br />
                       <ul> 
                        <li> addr - the address where the data is to be read
                        <li> size - she size of data to be read
                       </ul>

<b>Examples</b>
--------

See PoC

<b>Credits</b>
-------

Angelboy (@scwuaptx) and his slide's on File Structures - <a href="http://4ngelboy.blogspot.in/2017/11/play-with-file-structure-yet-another.html">Play with FILE Structure</a>
