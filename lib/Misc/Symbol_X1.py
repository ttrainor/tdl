# M. Newville Univ of Chicago (2006)
#
# -------------
# Modifications
# -------------
#
# 6-4-06 T2
# In SymbolTable.import_lib added a case for _scripts_
# If the lib module defines a list _scripts_ = [file1,file2]
# then these will be loaded (eg to define various defs or data..)
# Its assumed that these scripts live in the same directory as the
# library module.  
#
# 4-2-06 T2
# Modified symbolTable.initialize and symbolTable.import_lib
# to correctly handle strings as module names
#
# * 2-12-06 T2
# Added new methods for getting/putting to symbol table
# back to a single dictionary of symbols
#
#########################################################################

import types
import os
import random
import sys
import inspect
import re
from copy import deepcopy

from Num import Num
from Util import find_unquoted_char, split_delim, datalen, set_path
from Util import PrintExceptErr, PrintShortExcept, SymbolError, ConstantError

__version__  = '0.2'
random.seed(0)

# should these be moved to a more common place?
DataTypes = ('variable','defvar','object')
FuncTypes = ('pyfunc','defpro')
SymbolTypes = DataTypes + FuncTypes

# Default data groups
# search order will be dataGroup,funcGroup,mainGroup,builtinGroup,mathGroup,plotGroup

builtinGroup = '_builtin'
sysGroup     = '_sys'
mainGroup    = '_main'
mathGroup    = '_math'
plotGroup    = '_plot'
# groups that must always be present, and default search order
requiredGroups = (mainGroup,builtinGroup,sysGroup,mathGroup,plotGroup)
immutableGroups = (builtinGroup,sysGroup,mathGroup)

isValidName = re.compile(r'[a-zA-Z_\$][a-zA-Z_\$0-9]*').match

class Symbol:
    """
    basic container for all symbols: variables and functions.

    Each symbol has the following components:
       name      Simple Name used to access symbol (see note below)
       group     Simple Name for group name (see note below)
       value     python object for value
       type      name of Tdl variable type (not python type!)
       constant  boolean for whether value is fixed.
       desc      optional description (stores text formula for defvar)
       help      help string (say, for defpro)

       code      tdl code for defpro
       args      args for defpro
       kws       keywords for defpro
       cmd_out   method for processing output when a pyfunc of defpro
                 is run as a command.

    Symbol Names: Each symbol consists of a two part name:
       GROUP.NAME, where each of GROUP and NAME are 'Simple Names',
       matching:  [a-zA-Z_\$][a-zA-Z_\$0-9]*
      
    Types: Each symbol has one of the following types:
            variable   regular variable
            defvar     defined variable (expression retained)
            defpro     defined procedure (sequence of statement code)
            pyfunc     python function
            pyobj      other python object

    """

    name  = '***'
    def __init__(self, name, value=None, constant = False,
                 group='_builtin', type='variable',
                 desc=None, help=None, cmd_out=None,
                 code=None, args=None, kws=None):
        self.constant = False
        self.name     = name
        self.cmd_out  = cmd_out
        self.value    = value
        self.code     = code
        self.desc     = desc or ''
        self.help     = help or ''
        self.args     = args or []
        self.kws      = kws  or {}
        self.group    = group
        
        # check that type is valid
        if type not in SymbolTypes:
            raise SymbolError, 'cannot add symbol "%s" with type=%s' % (name,type)
        self.constant = constant
        self.type = type

    def getHelp(self):
        return self.help

    def getCode(self):
        return deepcopy(self.code)

    def __call__(self, *args,**kws):
        if self.type == 'pyfunc':
            x = {}
            x.update(self.kws) ; x.update(kws)
            # print 'CALL ', self.value,len(args), x
            val = self.value(*args,**x)
            return val
        else:
            return self.value

    def __cmdout__(self,val,**kws):
        x = {}
        x.update(self.kws) ; x.update(kws)
        if self.cmd_out:
            return self.cmd_out(val,**x)
        elif val is None:
            return None
        return str(val)
         
    def __setattr__(self, attr, val):
        """ here to prevent re-setting of constants"""
        if self.constant and attr == 'value':
            raise ConstantError,  'cannot set value of constant %s' % (self.name)
        self.__dict__[attr] = val


    def __repr__(self):
        name = "%s.%s" % (self.group,self.name)
        if self.type == 'variable':
            nelem = datalen(self.value)
            vtype = 'Variable'
            if self.constant: vtype = 'Variable (constant)'
            if nelem == 1:
                return "<%s %s: type=scalar, value=%s>" % (vtype,name,repr(self.value))
            else: 
                if type(self.value) == Num.ArrayType:
                    return "<%s %s: type=array, npts=%i, shape=%s>" % (vtype,name,len(self.value),self.value.shape)
                else:
                    t = str(type(self.value))[1:-1].replace('type','')
                    t.strip()
                    return "<%s %s: type=%s, len=%i>" % (vtype,name,t,nelem)
        elif self.type == 'defvar':
            return "<Defined Variable %s ='%s'>" % (name,self.desc)
        elif self.type == 'pyfunc':
            vtype = 'Function'
            if self.constant: vtype = 'Function (constant)'
            return "<%s %s>" % (vtype, name)
        elif self.type == 'defpro':
            args = ','.join(self.args)
            for k,v in  self.kws.items(): args = "%s,%s=%s" % (args,k,str(v))
            return "<Procedure %s: args='%s'>" % (name,args)
        return "<Symbol %s: %s : %s>" % (name, self.type,repr(self.value))
    

class SymbolTable:
    """
    table of symbols and namespaces storing all functions and variables
    """
    def __init__(self,libs=None,writer=sys.stdout,tdl=None, **kws):

        self.tdl    = tdl
        self.writer = writer
        self.load_libs = []
        init_libs = []
        init_libs = ['TdlBuiltins','TdlNumLib']  ##,'IO','Plotter']

        if libs is not None:  init_libs.extend(libs)
        self.initialize(init_libs,clearAll=True)

    def initialize(self,libs=None,clearAll=False):
        if clearAll:
            self.groups    = {}
            for i in requiredGroups:   self.groups[i] = {}
            self.dataGroup = mainGroup
            self.funcGroup = mainGroup
            self.setVariable('data_group',value=mainGroup,group=builtinGroup)
            self.setVariable('func_group',value=mainGroup,group=builtinGroup)
            self.setSearchGroups()
        if libs is not None:
            for lib in libs:
                self.import_lib(lib)

    def import_lib(self,lib):
        " import or reload module given module name or object"
        if lib is None: return None
        mod, msg = None, None
        syspath = self.getSymbolValue('_sys.path')
        # print syspath
        if syspath is not None:
            if type(syspath) == types.ListType:
                for pth in syspath: set_path(pth)
            elif type(syspath) == types.StringType:
                set_path(syspath)
        if type(lib) == types.StringType:
            try: 
                mod = __import__(lib)
                components = lib.split('.')
                for comp in components[1:]:
                    mod = getattr(mod, comp)
            except ImportError:
                msg = '    Error loading module %s:' % lib
        elif type(lib) == types.ModuleType:
            try:
                mod = reload(lib)
            except ImportError:
                msg = '    Error loading module %s:' % lib
        if mod is None:
            self.writer.write("    cannot load module %s !" % lib)
            if msg is not None: PrintShortExcept(msg)
            return None
        
        #
        # mod is now a real module, not a string of the module name

        title = getattr(mod,'title',mod.__name__)
        self.writer.write("    loading %s ..." % title)
        self.writer.flush()
        if mod not in self.load_libs: self.load_libs.append(mod)
        
        try:
            for nam,val in getattr(mod,'_consts_',{}).items():
                self.addVariable(nam,val,constant=True)
            for nam,val in getattr(mod,'_var_',{}).items():
                self.addSymbol(nam,value=val,type='variable')
            for nam,val in getattr(mod,'_func_',{}).items():
                cmdOut = None
                asCmd  = True
                func   = val
                if type(val) == types.TupleType:
                    func = val[0]
                    if len(val) > 1: cmdOut = val[1]
                    if len(val) > 2: asCmd  = val[3]
                x =self.addFunction(nam,func,cmd_out=cmdOut,as_cmd=asCmd)
            for nam in getattr(mod,'_scripts_',[]):
                try:
                    file_path = os.path.abspath(os.path.dirname(mod.__file__))
                    file_name = os.path.join(file_path,nam)
                    if os.path.exists(file_name) and os.path.isfile(file_name):
                        self.tdl.load_file(file_name)
                    else:
                        print "Warning: Cannot find lib script file: %s" % file_name
                except:
                    PrintExceptErr("Error loading script file '%s'"  % file_name)
            if self.tdl:
                for nam,val in getattr(mod,'_help_',{}).items():
                    self.tdl.help.add_topic(nam,val)
            import_msg = 'ok.'
        except ImportError:
            import_msg = 'import failed!'                

        self.writer.write(" %s\n" % import_msg)

    ### Name/type/util functions
    def split_name(self,name,group=None,use_default=True):
        """
        split symbol name into (group,name) tuple.

        if name is fully qualified (that is, includes a prefix as 'group.name'),
        (group,name) are simply returned

        if the name is not fully qualified (no '.' in the name), the supplied group name
        is used, if available.

        if the group name is not provided and use_default=True, the current dataGroup name
        will be supplied as group.

        common cases:
           g,n = split_name('dat1.x')               => 'dat1', 'x'
           g,n = split_name('x')                    => self.dataGroup, 'x'
           g,n = split_name('x',group='dat2')       => 'dat2', 'x'
           g,n = split_name('x',use_default=False)  => None, 'x'
        """
        try:
            name.strip()
        except (AttributeError,NameError):
            raise NameError, 'cannot use symbol name %s ' % name        
        
        if '.' in name:
            try:
                group,name=name.split('.')
                group.strip()
                name.strip()
            except:
                raise NameError, 'cannot use symbol name %s ' % name

        # default group name for group == None
        # always defaults to current data group
        if group is None and use_default: group = self.dataGroup
        return (group, name)

    ### symbol manipulation functions
    def addSymbol(self,name,value=None,group=None,type='variable',
                  code=None,desc=None,constant=False,**kws):
        """
        add generic symbol to symbol table
        to specify which group the symbol goes to, you can either use
        name = group.name or  use name=name, group=group
        """
        # print 'Add Symbol ', name, value, code        
        group, name = self.split_name(name,group=group)
        if isValidName(group) and isValidName(name):
            if group not in self.groups.keys():self.groups[group]={}
            if name in self.groups[group].keys():
                if self.groups[group][name].constant: return (None,None)
            self.groups[group][name] = Symbol(name,value=value,type=type,
                                           code=code,desc=desc,group=group,**kws)

            self.groups[group][name].constant = constant
            return (group,name)
        else:
            return (None,None)

    def delSymbol(self,name,group=None,override=False):
        """
        delete generic symbol (py function or variable) in symbol table.
        to specify which group you can either use
        name = group.name or  use name=name, group=group
        """
        group, name = self.hasSymbolName(name,group=group)
        if group in (None, builtinGroup): return
        if self.groups[group][name].constant and not override:   return

        self.groups[group].pop(name)
        if len(self.groups[group]) == 0 and group not in requiredGroups:
            self.delGroup(group)
            if self.dataGroup == group: self.dataGroup = mainGroup

    def getSymbol(self,name,groups=None,create=False):
        """
        return symbol (not just value!), creating if necessary
        name can be of form group.name or use just name and look in the list of supplied groups
        If type is in DataTypes default groups are [self.groupName,globalGroup,builtinGroup]
        If type is in FuncTypes default groups are [funcGroup]        
        creation puts symbol in the first group listed
        """
        # get group,name
        group, name = self.split_name(name,group=None,use_default=False)
        create_group = group

        # see if it exists, ie simple case with full name qualification:
        if group and self.groups.has_key(group):
            if self.groups[group].has_key(name):
                return self.groups[group][name]

        # if name was not fully qualified, then group=None, and
        # we need to search through groups
        if group is None:
            # search groups for name
            if groups is None:  groups = self.searchGroups
            create_group = groups[0]
            for group in groups:
                if self.groups[group].has_key(name):
                    return self.groups[group][name]

        if create:
            group, name = self.addSymbol(name,value=None,group=create_group,type='variable')
            return self.groups[group][name]
        return None

    def getSymbolValue(self,name,groups=None,default=None):
        sym = self.getSymbol(name,groups=groups,create=False)
        if sym:
            return sym.value
        else:
            return default

    #### Group manipulation and symbol checking
    def hasSymbol(self,name,group=None):
        " returns whether a symbol exists or not"
        return (None,None) != self.hasSymbolName(name,group=group)

    def hasSymbolName(self, name, group=None):
        " sees if a symbol exists, returning (group,name) if it does exist, or (None,None) if not."
        try:
            group, name = self.split_name(name,group=group,use_default=False)
        except NameError:
            return (None,None)
        if self.hasGroup(group):
            if name in self.groups[group].keys():   return (group,name)
        else:
            for grp in self.searchGroups:
                if name in self.groups[grp].keys(): return (grp,name)
        return (None,None)


    def hasGroup(self, group):
        " does this group exist? "
        return (self.groups.has_key(group) and  group is not None)

    def addGroup(self, group):
        " add a Group "
        group = group.strip()
        if isValidName(group):
            if not self.groups.has_key(group): self.groups[group] = {}
        return group

    def delGroup(self, group):
        " delete a group and all its symbols (except default groups)"
        group = group.strip()
        #if not group in (builtinGroup,globalGroup) and self.groups.has_key(group):
        #if self.groups.has_key(group) and group not in requiredGroups:
        #    self.groups.pop(group)
        # should we allow deleting required groups and just re-instate?
        # ie except for immutables??
        if group in immutableGroups:
            print "'%s' can not be deleted" % group
            return None
        elif self.groups.has_key(group):
            self.groups.pop(group)
            if group in requiredGroups:
                self.addGroup(group)
        else:
            print "Cant find group '%s'" % group
        return None

    def getDataGroup(self,group=None,create=True):
        "return group name, or default (self.dataGroup), and makes sure the group exist"
        if group is None: group = self.dataGroup
        if create:        group = self.addGroup(group)
        return group

    def getFuncGroup(self,group=None,create=True):
        "return group name, or default (self.dataGroup), and makes sure the group exist"
        if group is None: group = self.funcGroup
        if create:        group = self.addGroup(group)
        return group

    def setSearchGroups(self):
        self.searchGroups = [self.dataGroup]
        if self.funcGroup != self.dataGroup: self.searchGroups.append(self.funcGroup)
        for i in requiredGroups:
            if i not in self.searchGroups: self.searchGroups.append(i)
        return self.searchGroups
    
    def getSearchGroups(self):
        return self.searchGroups
            
    def setDataGroup(self, group):
        " set the current active group "
        group = group.strip()
        if not self.hasGroup(group): self.groups[group] = {}
        self.dataGroup = group
        self.setSearchGroups()        
        self.setVariable('data_group',value=group,group=builtinGroup)
        return group

    def setFuncGroup(self, group):
        " set the current active group "
        group = group.strip()
        if not self.hasGroup(group):  self.groups[group] = {}
        self.funcGroup = group
        self.setSearchGroups()        
        self.setVariable('func_group',value=group,group=builtinGroup)
        return group

    def addRandomGroup(self,prefix='',nlen= 8):
        """
        add a quasi-randomly generated group name that is
        'guaranteed' to be unique.
        If prefix is provided, the group name begins with
        that string
        returns the group name or None.
        """
        rand = random.randrange
        def randomName(n=8):
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
            return "_%s" % ''.join([chars[rand(0,len(chars))] for i in range(n)])
        if prefix is None: prefix = ''
        group = "%s%s" % (prefix,randomName(n = nlen))
        if self.hasGroup(group):
            ntry = 0
            while ntry<100:
                group = "%s%s" % (prefix,randomName(n = nlen))                
                if not self.hasGroup(group):break
                ntry = ntry + 1
                if (ntry % 20 == 0): nlen = nlen+1
        if self.hasGroup(group):
            return None
        self.groups[group] = {}
        return group
    
    def getAllData(self,group=None):
        """ if group = None get all data, otherwise get all data in group """
        data = []
        grouplist = [group]
        if group is None: grouplist = self.groups.keys()
        for group in grouplist:
            for name in self.groups[group].keys():
                if self.groups[group][name].type in DataTypes:
                    data.append(self.groups[group][name])
        return data

    def restoreData(self,blob):
        """ if group = None get all data, otherwise get all data in group """
        for sym in blob:
            g = sym.group
            n = sym.name
            if not self.hasGroup(g): self.addGroup(g)
            self.addVariable("%s.%s" % (g,n),value=deepcopy(sym.value),
                             type=sym.type,constant=sym.constant)
            
    def clearAllData(self,group=None):
        " delete data "
        # work on how this should operate...
        doomed = []
        if group is None:
            doomed = self.groups.keys()
        elif self.hasGroup(group):
            doomed = [group]
        for group in doomed:
            for name in self.groups[group].keys:
                if self.groups[group][name].type in DataTypes:
                    self.groups[group].pop(name)
            if len(self.groups[group]) == 0:
                self.delGroup(group)

    # generic add/delete/get func
    def hasFunc(self,name,group=None):
        try:
            group, name = self.hasSymbolName(name,group=group)
        except NameError:
            return False
        if group is None: return False
        return self.groups[group][name].type in FuncTypes

    def addFunction(self,name,func,ftype='pyfunc',code=None,
                    desc=None,as_cmd=True,cmd_out=None):
        "add function"
        if not func: return (None,None)
        if ftype not in FuncTypes:
            raise SymbolError, 'cannot add function %s ' % name

        fcn_kws = None
        try:
            if desc is None: desc = func.__doc__
            # look for 'tdl' argument --
            #    if present, add kw-arg to pass to function
            try:
                if (func.__name__.startswith('tdl') or 
                    'tdl' in inspect.getargspec(func)[0]):
                    fcn_kws = {'kws':{'tdl':self.tdl}}
            except TypeError:  # numpy ufuncs will raise a TypeError here...
                pass
        except:
            raise SymbolError, 'cannot add function %s ' % name

        if fcn_kws:
            return self.addSymbol(name,value=func,group=self.funcGroup,
                                  type=ftype,code=code,desc=desc,
                                  as_cmd=as_cmd,cmd_out=cmd_out,**fcn_kws)
        else:
            return self.addSymbol(name,value=func,group=self.funcGroup,
                                  type=ftype,code=code,desc=desc,
                                  as_cmd=as_cmd,cmd_out=cmd_out)
            
    def delFunc(self,name):
        "delete a function symbol"
        sym = self.getSymbol(name)
        if sym is not None:
            if sym.type in FuncTypes:
                return self.delSymbol(name)

    def getFunc(self,name):
        "get a function symbol"
        sym = self.getSymbol(name,groups=None,create=False)
        if sym is None: return None
        if sym.type in FuncTypes:
            return sym
        else:
            return None

    # variables (and const)
    def addVariable(self,name,value=None,type='variable',constant=False):
        " add variable (or const)"
        group,name = self.addSymbol(name,value=value,type=type,constant=constant)
        return (group,name)

    def getVariable(self,name,create=False):
        """ get variable (or const) """
        sym = self.getSymbol(name,create=create)
        if sym is not None: 
            if sym.type not in DataTypes:   sym = None
        return sym


    def getVariableCurrentGroup(self,name):
        """
        find variable (or const) in current group (or in group.name) or create it,
        WITHOUT looking to _builtin or _main or any other groups
        this should be used to lookup symbols for assignments
        """
        sym = self.getSymbol(name,groups=(self.dataGroup,),create=True)
        if sym is not None:
            if sym.type not in ('variable','defvar'):
                sym = None
        return sym

    def setVariable(self,name,value,type='variable',group=None,constant=False):
        return self.addSymbol(name,value=value,type=type,
                              group=group,constant=constant)

    # def variables
    def setDefVariable(self, name, code, desc,**kws):
        # print 'SetDEF VAR  ', name, code
        return self.addSymbol(name,value=None,type='defvar',code=code,desc=desc)
    
    # defined procedures    
    def addDefPro(self, name, code,desc=None, **kws):
        " add defined procedure "
        if desc is None: desc = name
        return self.addSymbol(name,value=name,group=self.funcGroup,
                              type='defpro',code=code,desc=desc,**kws)

    # functions to list stuff
    def listGroups(self):
        s = self.groups.keys()
        s.sort()
        return s

    def listSymbols(self):
        " return a dict of symbol names"
        all = {}
        groups = self.listGroups()
        for g in groups:
            sym = self.listGroupsSymbols(g)
            all.update({g:sym})
        return all

    def listGroupSymbols(self,group):
        if self.hasGroup(group):
            s = self.groups[group].keys()
            s.sort()
            return s
        else:
            return []

    def listData(self):
        "return a dict of data names as {grp:[name,name,...]}"
        all = {}
        glist = self.listGroups()
        for g in glist:
            s = self.listGroupSymbols(g)
            d = []
            for name in s:
                if self.groups[g][name].type in DataTypes:
                    d.append(name)
            all.update({g:d}) 
        return all

    def listFunctions(self):
        "return a dict of func names as {grp:[name,name,...]}"
        all = {}
        glist = self.listGroups()
        for g in glist:
            s = self.listGroupSymbols(g)
            fcn = []
            for name in s:
                if self.groups[g][name].type in FuncTypes:
                    fcn.append(name)
            all.update({g:fcn})
        return all

    def listDataGroup(self,group=None):
        "return a list of Data names in a group"
        if group is None: group = self.getDataGroup(group)
        all = self.listData()
        if group in all.keys():
            return all[group]
        else:
            return []
    
    def listFuncGroup(self,group=None):
        "return a list of Func names in a group"
        if group is None: group = self.getFuncGroup(group)
        all = self.listFunc()
        if group in all.keys():
            return all[group]
        else:
            return []

    # obsolete functions:
    def hasData(self,name,group=None):
        PrintShortExcept('symbolTable.hasData is obsolete')        

    def addData(self,name,value=None,code=None,type='variable'):
        PrintShortExcept('symbolTable.addData is obsolete')                
        
    def delData(self,name):
        PrintShortExcept('symbolTable.delData is obsolete')

    def getData(self,name):
        PrintShortExcept('symbolTable.getData is obsolete')        

    def SymbolType(name,group=None):
        PrintShortExcept('symbolTable.SymbolType is obsolete')