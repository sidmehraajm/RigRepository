from __future__ import print_function
from pymel.core import *
import sys
import maya.cmds as cmds
import maya.mel as mel
sys.path.append('B:/Eternal_Code_Directory')

import Procs

def EternalCodeUiDef():
	if pm.window( 'EternalCodeWin', exists = True):
		pm .deleteUI ('EternalCodeWin' ,window=True)
	
	if pm.windowPref( 'EternalCodeWin', exists = True):
		pm.windowPref ('EternalCodeWin' ,r=True)
	pm.window( 'EternalCodeWin', title="Object Random Populater", iconName='Short Name' ,h=250,w=300, s = 0 ,le = 20,te= 680)
    
	
 

	pm.showWindow ('EternalCodeWin')
	
EternalCodeUiDef()
















import pymel.core as pm
import random
Surface = pm.PyNode('nurbsPlane1')
Range = int(20)
for i in range(Range):

    RandomU = random.uniform(0.0,1)
    RandomV = random.uniform(0.0,1)
    print(str(RandomU),str(RandomV))
    fol = pm.createNode('transform',n=('TmpFol_'+str(i)),ss=1)
    folShape = pm.createNode('follicle',n  = fol.name()+'Shape',p = fol,ss=1)
    geo = Surface
    geo.local >> folShape.inputSurface
    geo.worldMatrix[0] >> folShape.inputWorldMatrix
    folShape.outRotate >> fol.rotate
    folShape.outTranslate >> fol.translate
    fol.inheritsTransform.set(False)
    folShape.parameterV.set(RandomV)
    folShape.parameterU.set(RandomU)
    sph = pm.polySphere(ch=0)
    pm.delete(pm.parentConstraint(fol,sph))
    pm.delete(fol)


    







