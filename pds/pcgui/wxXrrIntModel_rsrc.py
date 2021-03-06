data = {'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'XRR Interface Model',
          'size':(752, 750),
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit',
                  },
              ]
             },
             {'type':'Menu',
             'name':'menuHelp',
             'label':u'Help',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuHelpParams',
                   'label':u'Help on parameters',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'CheckBox', 
    'name':'DensityScale', 
    'position':(629, 42), 
    'checked':True, 
    'label':'Scale to Norm', 
    },

{'type':'Choice', 
    'name':'DensityFlag', 
    'position':(568, 38), 
    'size':(52, -1), 
    'items':[u'0', u'1', u'2'], 
    'stringSelection':'0', 
    },

{'type':'StaticText', 
    'name':'DensityNormLbl', 
    'position':(475, 42), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 8}, 
    'text':'Density Norm', 
    },

{'type':'StaticLine', 
    'name':'StaticLine13', 
    'position':(464, 39), 
    'size':(3, 24), 
    'layout':'horizontal', 
    },

{'type':'Button', 
    'name':'UpdateShell', 
    'position':(15, 3), 
    'size':(82, 26), 
    'label':'Shell Update', 
    },

{'type':'ComboBox', 
    'name':'Grp', 
    'position':(283, 4), 
    'size':(116, -1), 
    'items':[], 
    },

{'type':'ComboBox', 
    'name':'Model', 
    'position':(466, 4), 
    'size':(137, -1), 
    'items':[], 
    },

{'type':'Button', 
    'name':'Clear', 
    'position':(652, 4), 
    'size':(62, 25), 
    'label':'Clear', 
    },

{'type':'Choice', 
    'name':'Components', 
    'position':(136, 38), 
    'size':(116, -1), 
    'items':[], 
    },

{'type':'Choice', 
    'name':'Norm', 
    'position':(300, 38), 
    'size':(52, -1), 
    'items':[u'0', u'1', u'2', u'3'], 
    },

{'type':'CheckBox', 
    'name':'ScaleToNorm', 
    'position':(359, 42), 
    'label':'Scale to Norm', 
    },

{'type':'CheckBox', 
    'name':'AutoCalcDist', 
    'position':(175, 69), 
    'label':'Auto Calc Dist', 
    },

{'type':'Button', 
    'name':'DistInsert', 
    'position':(9, 92), 
    'size':(78, 22), 
    'label':'Insert', 
    },

{'type':'Button', 
    'name':'DistDelete', 
    'position':(9, 119), 
    'size':(78, 22), 
    'label':'Delete', 
    },

{'type':'Choice', 
    'name':'DistModel', 
    'position':(100, 115), 
    'size':(69, -1), 
    'items':[u'box', u'linear', u'erf', u'erfc', u'gauss', u'exp', u'expc'], 
    },

{'type':'TextField', 
    'name':'Zstart', 
    'position':(183, 115), 
    'size':(65, -1), 
    },

{'type':'TextField', 
    'name':'Zend', 
    'position':(260, 115), 
    'size':(66, -1), 
    },

{'type':'TextField', 
    'name':'Top', 
    'position':(369, 74), 
    'size':(366, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'Subs', 
    'position':(370, 104), 
    'size':(366, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'DistIndex', 
    'position':(11, 164), 
    'size':(45, -1), 
    'editable':False, 
    },

{'type':'TextField', 
    'name':'Param1', 
    'position':(64, 164), 
    'size':(117, -1), 
    },

{'type':'TextField', 
    'name':'Param2', 
    'position':(188, 164), 
    'size':(117, -1), 
    },

{'type':'TextField', 
    'name':'Param3', 
    'position':(312, 164), 
    'size':(117, -1), 
    },

{'type':'TextField', 
    'name':'Param4', 
    'position':(437, 164), 
    'size':(117, -1), 
    },

{'type':'TextField', 
    'name':'Param5', 
    'position':(561, 164), 
    'size':(117, -1), 
    },

{'type':'TextField', 
    'name':'SliderScale', 
    'position':(685, 182), 
    'size':(49, -1), 
    'text':'10.0', 
    },

{'type':'Slider', 
    'name':'P1slider', 
    'position':(64, 189), 
    'size':(117, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':100, 
    'min':-100, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':0, 
    },

{'type':'Slider', 
    'name':'P2slider', 
    'position':(188, 189), 
    'size':(117, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':100, 
    'min':-100, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':0, 
    },

{'type':'Slider', 
    'name':'P3slider', 
    'position':(312, 189), 
    'size':(117, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':100, 
    'min':-100, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':0, 
    },

{'type':'Slider', 
    'name':'P4slider', 
    'position':(437, 189), 
    'size':(117, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':100, 
    'min':-100, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':0, 
    },

{'type':'Slider', 
    'name':'P5slider', 
    'position':(561, 189), 
    'size':(117, 20), 
    'labels':False, 
    'layout':'horizontal', 
    'max':100, 
    'min':-100, 
    'tickFrequency':0, 
    'ticks':False, 
    'value':0, 
    },

{'type':'MultiColumnList', 
    'name':'DistList', 
    'position':(5, 208), 
    'size':(735, 111), 
    'backgroundColor':(255, 255, 255), 
    'columnHeadings':[u'Index', u'Dist', u'Zst', u'Zen', u'param1', u'param2', u'param3', u'param4', u'param5'], 
    'font':{'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 8}, 
    'items':[], 
    'maxColumns':20, 
    'rules':True, 
    },

{'type':'CheckBox', 
    'name':'AutoCalcRFY', 
    'position':(148, 333), 
    'checked':True, 
    'label':'Auto Calc R/FY', 
    },

{'type':'Button', 
    'name':'CalcDist', 
    'position':(14, 361), 
    'size':(60, 24), 
    'label':'Calc Dist', 
    },

{'type':'Button', 
    'name':'CalcR', 
    'position':(120, 361), 
    'size':(60, 24), 
    'label':'Calc R', 
    },

{'type':'Button', 
    'name':'CalcFY', 
    'position':(228, 361), 
    'size':(60, 24), 
    'label':'CalcFY', 
    },

{'type':'CheckBox', 
    'name':'PlotDensity', 
    'position':(18, 396), 
    'label':'Plot Density', 
    },

{'type':'CheckBox', 
    'name':'PlotComps', 
    'position':(18, 419), 
    'label':'Plot Comps', 
    },

{'type':'CheckBox', 
    'name':'PlotElements', 
    'position':(18, 440), 
    'label':'Plot Elements', 
    },

{'type':'CheckBox', 
    'name':'PlotRFY', 
    'position':(137, 396), 
    'checked':True, 
    'label':'Plot R/FY', 
    },

{'type':'CheckBox', 
    'name':'BarPlot', 
    'position':(137, 419), 
    'label':'Bar Plots', 
    },

{'type':'CheckBox', 
    'name':'PlotFracs', 
    'position':(137, 440), 
    'label':'Plot Frac', 
    },

{'type':'CheckBox', 
    'name':'HoldRFY', 
    'position':(241, 396), 
    'label':'Hold ', 
    },

{'type':'CheckBox', 
    'name':'PlotData', 
    'position':(241, 419), 
    'label':'Plot Data', 
    },

{'type':'CheckBox', 
    'name':'ShowTime', 
    'position':(241, 440), 
    'label':'Show calc time', 
    },

{'type':'Button', 
    'name':'DataUpdate', 
    'position':(430, 330), 
    'size':(52, 22), 
    'label':'Update', 
    },

{'type':'ComboBox', 
    'name':'Theta', 
    'position':(515, 364), 
    'size':(218, -1), 
    'items':[], 
    },

{'type':'ComboBox', 
    'name':'RData', 
    'position':(515, 396), 
    'size':(218, -1), 
    'items':[], 
    },

{'type':'ComboBox', 
    'name':'FYData', 
    'position':(515, 430), 
    'size':(218, -1), 
    'items':[], 
    },

{'type':'Button', 
    'name':'ParamsUpdate', 
    'position':(147, 464), 
    'size':(52, 22), 
    'label':'Update', 
    },

{'type':'TextField', 
    'name':'Energy', 
    'position':(182, 490), 
    'text':'10000.', 
    },

{'type':'TextField', 
    'name':'ConvWidth', 
    'position':(182, 517), 
    'text':'0.02', 
    },

{'type':'TextField', 
    'name':'SampLen', 
    'position':(182, 544), 
    'text':'50', 
    },

{'type':'TextField', 
    'name':'BeamVert', 
    'position':(182, 571), 
    'text':'0.01', 
    },

{'type':'TextField', 
    'name':'BeamHorz', 
    'position':(182, 598), 
    'text':'10.0', 
    },

{'type':'Choice', 
    'name':'AreaFlag', 
    'position':(182, 625), 
    'size':(52, -1), 
    'items':[u'0.0', u'1.0'], 
    'stringSelection':'0.0', 
    },

{'type':'TextField', 
    'name':'RefScale', 
    'position':(182, 652), 
    'text':'1.0', 
    },

{'type':'TextField', 
    'name':'FyEl', 
    'position':(588, 490), 
    'text':'-1.0', 
    },

{'type':'TextField', 
    'name':'FyEnergy', 
    'position':(588, 517), 
    'text':'6000.', 
    },

{'type':'TextField', 
    'name':'DetAngle', 
    'position':(588, 544), 
    'text':'90.0', 
    },

{'type':'TextField', 
    'name':'ThetaNorm', 
    'position':(588, 571), 
    'text':'1.0', 
    },

{'type':'Choice', 
    'name':'RoughFlag', 
    'position':(588, 598), 
    'size':(65, -1), 
    'items':[u'0.0', u'1.0'], 
    'stringSelection':'1.0', 
    },

{'type':'TextField', 
    'name':'DelZ', 
    'position':(588, 625), 
    'text':'10.0', 
    },

{'type':'TextField', 
    'name':'PDepth', 
    'position':(588, 652), 
    'text':'3.0', 
    },

{'type':'StaticLine', 
    'name':'StaticLine12', 
    'position':(16, 357), 
    'size':(320, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine11', 
    'position':(14, 388), 
    'size':(322, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'CalcLabel', 
    'position':(11, 329), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'text':'Calc / Plot', 
    },

{'type':'StaticText', 
    'name':'DataLbl', 
    'position':(370, 329), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'text':'Data', 
    },

{'type':'StaticText', 
    'name':'DistParamsLabel', 
    'position':(8, 67), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 10}, 
    'text':'Dist Parameters', 
    },

{'type':'StaticText', 
    'name':'SubsLabel', 
    'position':(336, 109), 
    'text':'Subs:', 
    },

{'type':'StaticText', 
    'name':'TopLabel', 
    'position':(336, 79), 
    'text':'Top:', 
    },

{'type':'StaticLine', 
    'name':'StaticLine10', 
    'position':(341, 138), 
    'size':(392, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'DistIndexLabel', 
    'position':(18, 146), 
    'text':'Index', 
    },

{'type':'StaticText', 
    'name':'FYDataLabel', 
    'position':(375, 433), 
    'text':'Fluorescent Yield Data', 
    },

{'type':'StaticText', 
    'name':'RDataLabel', 
    'position':(376, 404), 
    'text':'Reflectivity Data', 
    },

{'type':'StaticText', 
    'name':'SliderScaleLabel', 
    'position':(687, 145), 
    'size':(45, 31), 
    'text':'Slider Percent', 
    },

{'type':'StaticText', 
    'name':'ZendLbl', 
    'position':(275, 93), 
    'text':'Z end', 
    },

{'type':'StaticText', 
    'name':'ZstartLbl', 
    'position':(196, 93), 
    'text':'Z start', 
    },

{'type':'StaticText', 
    'name':'DistLabel', 
    'position':(102, 93), 
    'text':'Distribution', 
    },

{'type':'StaticText', 
    'name':'NormLbl', 
    'position':(259, 42), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 8}, 
    'text':'Norm', 
    },

{'type':'StaticLine', 
    'name':'StaticLine9', 
    'position':(6, 461), 
    'size':(733, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine8', 
    'position':(330, 69), 
    'size':(2, 71), 
    'layout':'horizontal', 
    },

{'type':'StaticText', 
    'name':'ReadLabel', 
    'position':(123, 6), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 10}, 
    'text':'Read Model', 
    },

{'type':'StaticText', 
    'name':'GrpLabel', 
    'position':(239, 8), 
    'text':'Group', 
    },

{'type':'StaticText', 
    'name':'ModelLabel', 
    'position':(419, 8), 
    'text':'Model', 
    },

{'type':'StaticText', 
    'name':'CompTitleText', 
    'position':(9, 39), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 11}, 
    'text':'Components', 
    },

{'type':'StaticText', 
    'name':'param1Label', 
    'position':(98, 145), 
    'text':'Param 1', 
    },

{'type':'StaticText', 
    'name':'param2Label', 
    'position':(222, 145), 
    'text':'Param 2', 
    },

{'type':'StaticText', 
    'name':'param3Label', 
    'position':(346, 145), 
    'text':'Param 3', 
    },

{'type':'StaticText', 
    'name':'param4Label', 
    'position':(471, 145), 
    'text':'Param 4', 
    },

{'type':'StaticText', 
    'name':'param5Label', 
    'position':(595, 145), 
    'text':'Param 5', 
    },

{'type':'StaticText', 
    'name':'ParamLabel', 
    'position':(10, 462), 
    'font':{'style': 'bold', 'faceName': u'Tahoma', 'family': 'sansSerif', 'size': 12}, 
    'text':'Parameters', 
    },

{'type':'StaticText', 
    'name':'ThetaLabel', 
    'position':(377, 370), 
    'text':'Theta (deg)', 
    },

{'type':'StaticText', 
    'name':'EnergyLabel', 
    'position':(26, 490), 
    'text':'Energy (eV)', 
    },

{'type':'StaticText', 
    'name':'ConvWidthLabel', 
    'position':(26, 517), 
    'text':'Convolution Width (deg)', 
    },

{'type':'StaticText', 
    'name':'SampleLenLabel', 
    'position':(26, 544), 
    'text':'Sample Length (mm)', 
    },

{'type':'StaticText', 
    'name':'BeamVertLabel', 
    'position':(26, 571), 
    'text':'Beam Vert (mm)', 
    },

{'type':'StaticText', 
    'name':'BeamHorzLabel', 
    'position':(26, 598), 
    'text':'Beam Horz (mm)', 
    },

{'type':'StaticText', 
    'name':'AreaFlagLabel', 
    'position':(26, 625), 
    'text':'Model Area Dependence ', 
    },

{'type':'StaticText', 
    'name':'RefScaleLabel', 
    'position':(26, 652), 
    'text':'Reflectivity Scale', 
    },

{'type':'StaticText', 
    'name':'FyIdxLabel', 
    'position':(383, 490), 
    'text':'FY Element (symbol or Z)', 
    },

{'type':'StaticText', 
    'name':'FyEnergyLabel', 
    'position':(383, 517), 
    'text':'FY Energy (eV or line)', 
    },

{'type':'StaticText', 
    'name':'DetAngleLabel', 
    'position':(383, 544), 
    'text':'FY Detector Angle (deg)', 
    },

{'type':'StaticText', 
    'name':'TextNormLabel', 
    'position':(383, 571), 
    'text':'FY Normalization Angle (deg)', 
    },

{'type':'StaticText', 
    'name':'RoughFlagLabel', 
    'position':(383, 598), 
    'text':'RoughnessFlag', 
    },

{'type':'StaticText', 
    'name':'DelZLabel', 
    'position':(383, 625), 
    'text':'Integration Delta Z (ang)', 
    },

{'type':'StaticText', 
    'name':'PDepthLabel', 
    'position':(383, 652), 
    'text':'FY Base Penetration Depth Factor', 
    },

{'type':'StaticLine', 
    'name':'StaticLine7', 
    'position':(355, 474), 
    'size':(3, 199), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine6', 
    'position':(8, 679), 
    'size':(733, 4), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine5', 
    'position':(355, 333), 
    'size':(3, 118), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine4', 
    'position':(4, 320), 
    'size':(737, 5), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine3', 
    'position':(112, 4), 
    'size':(3, 26), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine2', 
    'position':(8, 66), 
    'size':(727, -1), 
    'layout':'horizontal', 
    },

{'type':'StaticLine', 
    'name':'StaticLine1', 
    'position':(8, 33), 
    'size':(728, 3), 
    'layout':'horizontal', 
    },

] # end components
} # end background
] # end backgrounds
} }
