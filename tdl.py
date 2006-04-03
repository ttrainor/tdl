#!/usr/bin/python
############################################################################
# T. Trainor
#
# -------------
# Modifications
# -------------
#
#
############################################################################

import os, string, sys, getopt
import ConfigParser
import tdl

##############################################################
# test for command line switches
startup   = True
use_wxGUI = False
fname     = ''
debug = False

opts, args = getopt.getopt(sys.argv[1:], "whnfd:")
for o, a in opts:
    if o == '-w':
        use_wxGUI = True
    elif o == '-n':
        use_wxGUI = False
    elif o == '-f':
        fname = a
    elif o == '-d':
        debug = True
    elif o == '-h':
        print 'Startup options for tdl:'
        print '-h:  help'
        print '-w:  use wx GUI'
        print '-n:  no GUI, plot with tk'
        print '-ffname: execute fname on startup'
        print '-d: debug on'
        startup = False
        
##############################################################
# startup
intro = None
if startup:
    #### get TDL_PATH if it exist and append to sys.path
    if os.environ.has_key('TDL_PATH'):
        intro = "Tdl path settings:\n"
        p = os.environ['TDL_PATH']
        tmp = string.split(p,os.pathsep)
        for s in tmp:
            sys.path.append(s)
            intro = "%s%s\n" % (intro,s)
        sys.path.append('.')
        INI_file = os.path.join(os.environ['TDL_PATH'],'tdl.ini')
        config = ConfigParser.ConfigParser()
        config.read('tdl.ini')
        libs = []
        for libname in config.get('LibModule','Lib').split(','):
            l = libname.strip()
            if len(l) > 0: libs.append(l)
    else:
        libs = []

    if use_wxGUI == False:
        t = tdl.shell(libs=libs,debug=debug,intro=intro)
        t.cmdloop()
    elif use_wxGUI == True:
        # tdl gets started from within the wxGUI
        import tdl_wxGUI
        tdl_wxGUI.tdl = tdl
        tdl_wxGUI.libs = libs
        tdl_wxGUI.intro = intro
        tdl_wxGUI.debug = debug
        # this needs to be fixed bf compile
        rsrc = os.environ['WX_RSRC']
        # looks like dir gets reset when call application
        work_dir = os.getcwd()
        # the wxGUI code handles creation of dsi and plot_init...
        gui = tdl_wxGUI.model.Application(tdl_wxGUI.tdl_wxGUI, aFileName=rsrc)
        os.chdir(work_dir)
        gui.MainLoop()

    

    
