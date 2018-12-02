from os import system

try:
    import pwn
except ImportError:
    print "Please install pwntools first"
    quit()

path=pwn.__file__

toedit=path[:-1*(path[::-1].find('/'))]+'toplevel.py'
copypath=path[:-1*(path[::-1].find('/'))].replace('pwn/','pwnlib/')
system('cp ./FilePointer.py '+copypath)

file=open(toedit).read()

write=file.find('from pwnlib import *')+len('from pwnlib import *\n')
out=file[:write]+"from pwnlib.FilePointer import *\n"+file[write:]

open(toedit,'w').write(out)
