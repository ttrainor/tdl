#!/usr/bin/env
# M. Newville Univ of Chicago (2005)
#
# --------------
# Modifications
# --------------
#
#  
##########################################################################
import Num
from Num import num_version, ndarray
import version
import os
import sys
import types
import time

from Util import show_list, show_more, datalen, unescape_string, list2array
from Util import set_path, verify_tdl
from Symbol import isGroup, isSymbol, Group

title = "builtin library functions"

HelpBuiltins = """
  Builtin Functions: Overview

  additional help is available on these topics:
     help i/o      help on input/output (creating,writing,reading files)
     help os       help on interacting with the operating system (ls,path,...)
     help import   additional help on importing 
        
  Brief description of builtin functions:
     datagroup :  set default data group
         tdl> datagroup('mydata')

     funcgroup :  set default function group
         tdl> funcgroup('myfunctions')
         
     load      :  load and run a tdl program from external file
         tdl> load('program.tdl')
         
     import    :  import python modules
         tdl> import('module.py')        # imports (or re-imports) python module
         tdl> import()                   # re-imports all defined python modules
         
     eval      :  evaluate a tdl expression or statement
         tdl> eval('1/5')
         0.2
         tdl> eval(' x = sqrt(3)')
         tdl> print x
         1.73205080757 

     setvar    :  set a variable from a string, returns fully qualified name
         tdl> setvar('x',3)
         _main.x
         tdl> print x
         3.0

     type      :  returns the type of a variable

     debug      -
     abs        -
     max        -
     min        -
     len        -
     list       -

     strfind    -
     strsplit   -

     dictkeys   -
     dictvals   -
     dictitems  -

     cd         -
     pwd        -
     more       -
     path       -
     ls         -

"""


HelpIO = """
  Builtin Functions for Input/Output (creating,writing,reading files):

  = open(file,mode)
      tdl> f = open('myfile.txt','w')

  will open the file 'myfile.txt' for writing (and killing any existing file
  with that name!).  The value returned from open() is called the *file handle*
  and is a special value (a python object) that won't make sense as any other
  type.  But you can use a file handle to read, write, and close a file.

     tdl> write(f, 'a string\\n')
     tdl> write(f, 'another line.\\n')
     tdl> close(f)

  Note that writing a string to a file requires the newlines to be explicitly
  included.

  You can also read from an existing file if you open it in 'read mode':
     tdl> f = open('myfile.txt', 'r')
     tdl> x1 = readline(f)
     tdl> x2 = readline(f)
     tdl> print x1
     a string
     tdl> print x2
     another line

     tdl> close(f)
      
"""

HelpOS = """
  Builtin Functions for Interacting with the operating system

  ls

  more
  
  pwd

  cd

  !
  
"""

HelpImport = """
   Importing Python modules
"""

#################################################################
def _help(arg='',tdl=None,**kw):
    verify_tdl(tdl,name='help')
    tdl.help.help(arg)

def _show(arg='',tdl=None,**kw):
    verify_tdl(tdl,name='show')
    if len(arg.strip())==0:
        tdl.help.show_topgroups_fmt()
    elif arg == "-l":
        tdl.help.show(arg='',extended=True)    
    else:
        tdl.help.show(arg)

def _dir(x,tdl=None,**kws):
    ll = dir(x)
    return ll

def _dir_cmd(ll,**kws):
    return show_list(ll,ncol=1)

def _dictkeys(x):
    "return list of dictionary keys"
    if type(x) == types.DictType:
        return x.keys()
    else:
        return []

def _dictitems(x):
    "return list of dictionary items"
    if type(x) == types.DictType:
        return [list(i) for i in x.items()]
    else:
        return []
    
def _dictpop(x,key):
    "return list of dictionary keys"
    if type(x) == types.DictType:
        return x.pop(key)
    else:
        return ''

def _dictvals(x):
    "return list of dictionary keys"
    if type(x) == types.DictType:
        return x.values()
    else:
        return []    

def _pop(x,item=None):
    "???  pop last element from a list"

    if type(x) == ndarray: x = x.tolist()
    if type(x) == types.ListType:
        out = x.pop()
        x = x
    return out, x

def _len(x):
    "return length of data"
    return datalen(x)

def _list(x):
    "convert argument to a list type"
    try:
        return list(x)
    except TypeError:
        return x

def _listappend(x,val):
    "append a value to a list"
    if type(x) == ndarray:
        x = x.tolist()
        x.append(val)
        return list2array(x)
    if type(x) == types.ListType:
        x.append(val)
        return x

def _listjoin(x,y):
    "join two lists"    
    "return list of dictionary items"
    if type(x) == ndarray:
        x = x.tolist()
        if type(y) == ndarray: y = y.tolist()
        if type(y) == types.ListType:
            x.extend(y)
        elif datalen(y) == 1:
            x.append(y)
        return list2array(x)
    if type(x) == types.ListType:
        if type(y) == ndarray: y = y.tolist()
        if type(y) == types.ListType:
            x.extend(y)
        elif datalen(y) == 1:
            x.append(y)
        #return list2array(x)
        return x
    
def _listreverse(x):
    "join two lists"    
    "return list of dictionary items"
    if type(x) == ndarray:
        x = x.tolist()
        x.reverse()
        return list2array(x)
    if type(x) == types.ListType:
        x.reverse()
        #return list2array(x)
        return x

def _listsort(x):
    "join two lists"    
    "return list of dictionary items"
    if type(x) == ndarray:
        return x.sort()
    if type(x) == types.ListType:
        return x.sort()
        #return list2array(x)

def _strsplit(var,sep=' '):
    "split a string"
    if type(var) != types.StringType:
        print ' %s is not a string ' % var
        return None
    return var.split(sep)

def _strfind(var,sub):
    "string find"
    if type(var) != types.StringType:
        print ' %s is not a string ' % var
        return None
    return var.find(sub)

def _strchomp(var):
    "string find"
    # print 'var ', var, type(var), var[:-1]
    if type(var) != types.StringType:
        print ' %s is not a string ' % var
        return None
    return var[:-1]

def _strstrip(var,delim=None):
    "string find"
    if type(var) != types.StringType:
        print ' %s is not a string ' % var
        return None
    if delim is None:
        return var.strip()
    else: 
        return var.strip(delim)

def _ls(arg= '.',**kws):
    " return list of files in the current directory "
    from glob import glob
    arg.strip()
    if type(arg) != types.StringType or len(arg)==0: arg = '.'
    if os.path.isdir(arg):
        ret = os.listdir(arg)
    else:
        ret = glob(arg)
    if sys.platform == 'win32':
        for j in range(len(ret)):
            ret[j] = ret[j].replace('\\','/')
    return ret

def _ls_cmdout(x,ncol=None,**kws):
    " output for ls "
    return show_list(x,ncol=ncol)

def _cwd(x=None):
    "return current working directory"
    ret = os.getcwd()
    if sys.platform == 'win32':
        ret = ret.replace('\\','/')
    return ret

def _cd(name):
    "change directorty"
    name = name.strip()
    if name:
        try:
            os.chdir(name)
        except:
            print "Directory '%s' not found" % name
    ret = os.getcwd()
    if sys.platform == 'win32':
        ret = ret.replace('\\','/')
    return ret

def _more(name,pagesize=24):
    "list file contents"
    try:
        f = open(name)
        l = f.readlines()
        f.close()
        show_more(l,filename=name,pagesize=pagesize)
    except IOError:
        print "cannot open file: %s." % name
        return

def _type(x):
    "return data type of data"
    typecodes = {types.StringType:'string',
                 types.IntType: 'int',
                 types.LongType:'int',
                 types.FloatType:'float',
                 types.ComplexType:'complex',
                 types.ListType:'list',
                 types.DictType:'dict',
                 ndarray:'array'}
    t = type(x)
    if t in typecodes.keys(): return typecodes[t]
    if t in Num.typeDict.values(): return t
    if isGroup(x): return 'group'
    if isSymbol(x): return x.type
    return 'object'

def tdl_path(pth=None,recurse=False,tdl=None,**kw):
    "modify or show python path"
    verify_tdl(tdl,'path')
    if not pth:
        return show_list(sys.path)
    else:
        set_path(pth=pth,recurse=recurse)
        tdl.setVariable('_sys.path', sys.path)
    return

def tdl_input(prompt='',tdl=None,**kw):
    "get a line of raw input"
    #return raw_input(prompt)
    verify_tdl(tdl,'input')
    tdl.output.write(prompt)
    tdl.output.flush()
    line = tdl.input.readline()
    return line

def tdl_open(filename,mode='r',tdl=None,**kw):
    " open a file "
    return open(filename,mode=mode)

def tdl_close(file,tdl=None,**kw):
    " close a file "
    if type(file) == types.FileType:
        return file.close()
    else:
        return False

def tdl_write(file,s,tdl=None,**kw):
    " write a string to a file "
    if type(file) == types.FileType:        
        return file.write(unescape_string(s))

def tdl_flush(file,tdl=None,**kw):
    " flush a file "
    if type(file) == types.FileType: return file.flush()

def tdl_read(file,size=None,tdl=None,**kw):
    " read from a file "
    if type(file) == types.FileType: return file.read(size=size)

def tdl_readline(file,size=None,tdl=None,**kw):
    " readline a file "
    if type(file) == types.FileType: return file.readline(size=size)    

def tdl_readlines(file,tdl=None,**kw):
    " read all lines of text from a file "
    if type(file) == types.FileType: return file.readlines()

def tdl_seek(file,offset,whence=None,tdl=None,**kw):
    " read all lines of text from a file "
    if type(file) == types.FileType: return file.seek(offset,whence=whence)        

def tdl_tell(file,offset,whence=None,tdl=None,**kw):
    " read all lines of text from a file "
    if type(file) == types.FileType: return file.tell()

def tdl_set_debug(debug=None,tdl=None,**kw):
    verify_tdl(tdl, 'set_debug')
    if debug == None or debug == "":
        #debug = not tdl.debug
        if tdl.debug > 0:
            debug = 0
        elif tdl.debug == 0:
            debug = 1
        else:
            debug = 0
    tdl.set_debug(debug)
    return None

def tdl_load(fname, tdl=None,group=None,debug=False,**kw):
    " load file of tdl code"

    verify_tdl(tdl, 'load',msg='loading file %s' % fname)
    symTab = tdl.symbolTable
    if not os.path.isfile(fname):
        ftdl = '%s.tdl' % fname
        if os.path.isfile(ftdl):
            fname = ftdl
        else:
            print 'file error: cannot find file to load for %s ' % fname
            return None

    _locgroup = None
    _modgroup = None
    if group is None:
        group = os.path.basename(os.path.splitext(fname)[0])
    else:
        _locgroup = symTab.LocalGroup
        _modgroup = symTab.ModuleGroup
        symTab.addGroup(group,toplevel=True,status='module')
        symTab.LocalGroup = group
        symTab.ModuleGroup = group

    tdl.load_file(fname)
    tdl.run()
    if _locgroup is not None: symTab.LocalGroup = _locgroup
    if _modgroup is not None: symTab.ModuleGroup = _modgroup

    if debug: print 'load done.'
    return

def tdl_import(lib='',tdl=None,debug=False,reloadAll=False,clearAll=False,**kw):
    """
    import python modules that define tdl functions,
    import()               # re-imports all previously defined modules
    import('x.py')         # imports new module x.py
    ##import(clearAll=True)  # re-imports modules AND clears all data  
    """
    verify_tdl(tdl, 'import',msg='trying to import %s' % lib)
    if lib:
        tdl.symbolTable.import_lib(lib)
    else:
        tdl.symbolTable.reimport_libs()
    if debug: print 'import done.'

def tdl_eval(expr, tdl=None,debug=False,**kw):
    " evaluate tdl expression"
    verify_tdl(tdl, 'eval',msg='trying to eval %s' % expr)
    return tdl.eval(expr)

def tdl_setvar(name,val,tdl=None,debug=False,**kws):
    "set default group"
    verify_tdl(tdl, 'setvar',msg='trying to setvar %s' % name)
    return tdl.symbolTable.setVariable(name,val,**kws)

def tdl_newgroup(name=None,tdl=None,toplevel=True,debug=False,**kw):
    "add a group"
    verify_tdl(tdl, 'newgroup')
    if name == None: return
    if len(name.strip()) == 0: return
    tdl.symbolTable.addGroup(name,toplevel=toplevel,**kw)
    #return tdl.symbolTable.addGroup(name,toplevel=toplevel,**kw)
    #return Group(name='_',toplevel=toplevel,vars=kw)

def tdl_set_data_group(name=None,toplevel=True,tdl=None,**kw):
    "set default data group"
    verify_tdl(tdl, 'datagroup')
    if name == None:
        return tdl.symbolTable.LocalGroup        
    if len(name.strip()) == 0:
        return tdl.symbolTable.LocalGroup
    
    if tdl.symbolTable.hasGroup(name):
        tdl.symbolTable.LocalGroup = name
    else:
        try:
            g = tdl.symbolTable.addGroup(name,toplevel=toplevel,**kw)
            tdl.symbolTable.LocalGroup = name
        except:
            print "%s is an invalid group" % name
    return 

def tdl_set_module_group(name=None,toplevel=True,tdl=None,**kw):
    "set default data group"
    verify_tdl(tdl, 'funcgroup')
    if name == None:
        return tdl.symbolTable.ModuleGroup        
    if len(name.strip()) == 0:
        return tdl.symbolTable.ModuleGroup

    if tdl.symbolTable.hasGroup(name):
        tdl.symbolTable.ModuleGroup = name
    else:
        try:
            g = tdl.symbolTable.addGroup(name,toplevel=toplevel,**kw)
            tdl.symbolTable.ModuleGroup = name
        except:
            print "%s is an invalid group" % name
    return 
    
def tdl_delvar(name,tdl=None,**kw):
    "delete a variable "
    verify_tdl(tdl, 'delvar',msg='trying to delete variable %s' % name)
    return tdl.symbolTable.delSymbol(name)

def tdl_func_as_cmd(name,tdl=None):
    "allow functions to act as commands"
    verify_tdl(tdl, 'func as cmd')

    if tdl.symbolTable.hasFunction(name):
        sym = tdl.symbolTable.getSymbol(name)
        sym.as_cmd = True
    return
##    
## save / restore state
##
def tdl_savestate(fname, tdl=None,debug=False,**kw):
    " save program state to a file"
    verify_tdl(tdl,'savestate')
    if debug: print 'savestate ... ', fname

    dat = tdl.symbolTable.getAllData()

    d = {'save_version': 2,
         'title':        'TDL Save Set',
         'tdl_version':  version.version,
         'num_version':  num_version,
         'os_name':      os.name,
         'os_environ':   os.environ,
         'timestamp':    time.time(),
         'data_table':   dat}

    import cPickle
    try:
        f = open(fname,'w')
        cPickle.dump(d,f)
        f.close()
    except:
        print 'error saving state to %s ' % fname        

def tdl_restorestate(fname, tdl=None,debug=False,**kw):
    " restore state from a file"

    verify_tdl(tdl,'restorestate')
    if debug: print 'restorestate .... ', fname
    if not os.path.isfile(fname):
        print 'file error: cannot find file %s ' % fname
        return None        
    try:
        f = open(fname)
        import cPickle
        d = cPickle.load(f)
        f.close()
    except:
        print 'error restoring state from %s ' % fname        
    #
    isOK = True
    try:
        vers = d['save_version']
        title= d['title']
        tver = d['tdl_version']
        data = d['data_table']
        isOk = isOK and (d['title'] == 'TDL Save Set')
        isOk = isOK and (int(d['save_version']) >= 2)
    except:
        isOK = False

    if isOK:
        tdl.symbolTable.restoreData(data)
    else:
        print '%s is not a proper TDL save file' % fname

##    
## Simple python interface

def _python(arg=None,tdl=None,**kws):
    """Execute raw python commands
       >>python arg
       >>python

    Executes the commands passed and return, or (if no command is given)
    enter an interactive prompt.
    """
    verify_tdl(tdl, 'python',msg='executing python command %s' % arg)
    exec_namespace = {'tdl':tdl,'sym':tdl.symbolTable}
    if arg:
        try:
            #ret = eval(arg.strip())
            #exec arg.strip() in tdl.PythonNameSpace
            exec arg.strip() in exec_namespace
            return
        except:
            tdl.ShowError('Python Exception')
            return 

    print 'Python shell, type ret to return'
    while True:
        arg = raw_input("python>>")
        #tdl.output.write("python>>")
        #tdl.output.flush()
        #arg = tdl.input.readline()
        arg.strip()
        if arg == 'ret':
            return
        elif arg == '':
            pass
        elif arg[0:2] == 'p ':
            try:
                arg = 'print %s' % arg[1:]
                exec arg in exec_namespace
            except:
                tdl.ShowError('Python Exception')
        else:
            try:
                exec arg in exec_namespace
            except:
                tdl.ShowError('Python Exception')
    return
    

#################################################################
# Load the functions
#################################################################

# constants to go into _builtin name space
_consts_ = {"_builtin.True": True, "_builtin.False":False, "_builtin.None":None}

_help_  = {'builtins': HelpBuiltins,
           'i/o':HelpIO,
           'os': HelpOS,
           'import': HelpImport,
           }

#_var_  = {'_builtin.data_group': None }


# functions to add to namespace
_func_ = {'_builtin.load':(tdl_load, None),
          '_builtin.import':(tdl_import, None),
          '_builtin.eval':(tdl_eval,None),
          '_builtin.setvar':(tdl_setvar,None),
          '_builtin.newgroup':(tdl_newgroup,None),
          '_builtin.datagroup':(tdl_set_data_group,None),
          '_builtin.funcgroup':(tdl_set_module_group,None),
          '_builtin.delete':tdl_delvar,
          '_builtin.debug':(tdl_set_debug,None),
          "_builtin.cd":(_cd,None),
          "_builtin.pwd":(_cwd,None),
          "_builtin.more":(_more,None),
          "_builtin.ls":(_ls,_ls_cmdout),
          "_builtin.abs":(abs,None),
          "_builtin.max":(max,None),
          "_builtin.min":(min,None),
          "_builtin.len":(_len,None),
          "_builtin.list":(_list,None),
          "_builtin.strfind":(_strfind,None),
          "_builtin.strsplit":(_strsplit, None),
          "_builtin.strstrip":(_strstrip, None),
          "_builtin.strchomp":(_strchomp, None),
          "_builtin.type":(_type,None),
          "_builtin.dictkeys":(_dictkeys,None),
          "_builtin.dictvals":(_dictvals,None),
          "_builtin.dictitems":(_dictitems,None),
          "_builtin.append":(_listappend,None),
          "_builtin.join":(_listjoin,None),
          "_builtin.reverse":(_listreverse,None),
          "_builtin.sort":(_listsort,None),
          "_builtin.get_timestamp":(time.time,None),
          "_builtin.sleep":(time.sleep,None),
          "_builtin.open":tdl_open,
          "_builtin.close":tdl_close,
          "_builtin.write":tdl_write,
          "_builtin.read":tdl_read,
          "_builtin.readlines":tdl_readlines,
          "_builtin.help":(_help,None),
          "_builtin.show":(_show,None),
          "_builtin.input":(tdl_input,None),
          "_sys.set_path":(tdl_path,None),
          "_builtin.save_state":(tdl_savestate,None),
          "_builtin.restore_state":(tdl_restorestate,None),
          "_builtin.python":(_python,None),
          "_builtin.dir":(_dir,_dir_cmd)
          }

if __name__ == '__main__':
    print title