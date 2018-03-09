length=0
size='size'
name='name'

variables={
    0:{name:'flags',size:length},
    1:{name:'_IO_read_ptr',size:length},
    2:{name:'_IO_read_end',size:length},
    3:{name:'_IO_read_base',size:length},
    4:{name:'_IO_write_base',size:length},
    5:{name:'_IO_write_ptr',size:length},
    6:{name:'_IO_write_end',size:length},
    7:{name:'_IO_buf_base',size:length},
    8:{name:'_IO_buf_end',size:length},
    9:{name:'_IO_save_base',size:length},
    10:{name:'_IO_backup_base',size:length},
    11:{name:'_IO_save_end',size:length},
    12:{name:'markers',size:length},
    13:{name:'chain',size:length},
    14:{name:'fileno',size:4},
    15:{name:'_flags2',size:4},
    16:{name:'_old_offset',size:length},
    17:{name:'_cur_column',size:2},
    18:{name:'_vtable_offset',size:1},
    19:{name:'_shortbuf',size:1},
    20:{name:'unknown1',size:-4},
    21:{name:'_lock',size:length},
    22:{name:'_offset',size:8},
    23:{name:'_codecvt',size:length},
    24:{name:'_wide_data',size:length},
    25:{name:'unknown2',size:length},
    26:{name:'vtable',size:length}
}

defaults=[
 'chain',
 '_lock',
 '_wide_data'
]

def get_defaults(null):
        var={}
        for i in defaults:
            var[i]=null
        return var

def update_var(l):
    var={}
    for i in variables:
        var[variables[i]['name']]=variables[i]['size']
    for i in var:
        if var[i]<=0:
            var[i]+=l
    if l==4:
        var['unknown2']=56
    else:
        var['unknown2']=48
    return var

def packit(s,l=8):
    if l==0:
        return ''
    return  hex(s).replace('0x','').rjust(2*l,'0').replace('L','').decode('hex')[::-1].ljust(l,'\x00')

class FileStructure(dict):
    vars_=[]
    length={}
    arch=64

    def __init__(self,null=0,arch=64):
            self.vars_=[variables[i]['name'] for i in sorted(variables.keys())]
            self.update({v:0 for v in self.vars_})
            self.update(get_defaults(null))
            self['_offset']=0xffffffffffffffff
            if arch==32 or arch==64:
                self.arch=arch
            else:
                print " [-] Unknown architecture %i" % arch
            if arch==32:
                self.length=update_var(4)
                self['_old_offset']=0xffffffff
            else:
                self.length=update_var(8)
                self['_old_offset']=0xffffffffffffffff

    def __setattr__(self,item,value):
        if item in FileStructure.__dict__:
            object.__setattr__(self,item,value)
        else:
            self.set_vars(item,value)

    def __getattr__(self,item):
        return self[item]

    def __setitem__(self,item,value):
        if item not in self.vars_:
            print " [-] Unknown variable %r" % item
        return super(FileStructure,self).__setitem__(item,value)

    def __repr__(self):
        d=self.sort_str()
        return "{"+ "\n".join((" %r:%s"%(k,v)) for k,v in d)+"}"

    def __len__(self):
        return len(str(self))

    def __str__(self):
        structure=''
        for val in self.vars_:
            if type(self[val]) is str:
                if self.arch==32:
                    structure+=self[val].ljust(4,'\x00')
                else:
                    structure+=self[val].ljust(8,'\x00')
            else:
                structure+=packit(self[val],self.length[val])
        return structure

    def sort_str(self):
        d=self.items()
        d.sort(key=lambda x:self.vars_.index(x[0]))
        return d

    def set_vars(self,item,value):
        self[item]=value

    def struntil(self,v):
        if v not in self.vars_:
            return ''
        structure=''
        for val in self.vars_:
            if type(self[val]) is str:
                if self.arch==32:
                    structure+=self[val].ljust(4,'\x00')
                else:
                    structure+=self[val].ljust(8,'\x00')
            else:
                structure+=packit(self[val],self.length[val])
            if val==v:
                break;
        return structure[:len(structure)-1]

    def write(self,addr=0,size=0):
        self['flags'] &=~8
        self['flags'] |=0x800
        self['_IO_write_base'] = addr
        self['_IO_write_ptr'] = addr+size
        self['_IO_read_end'] = addr
        self['fileno'] = 1
        return self.struntil('fileno')

    def read(self,addr=0,size=0):
        self['flags'] &=~4
        self['_IO_read_base'] = 0
        self['_IO_read_ptr'] = 0
        self['_IO_buf_base'] = addr
        self['_IO_buf_end'] = addr+size
        self['fileno'] = 0
        return self.struntil('fileno')

if __name__=='__main__':
    from IPython import embed

    q=FileStructure(null=0x10203040)
    embed()
