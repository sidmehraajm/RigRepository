from pymel.core import *
import sys
import maya.cmds as cmds
import maya.mel as mel
def ZeroOut(obj):
    
    try:
        grp = pm.createNode('transform',n = obj + '_Group')
        pm.delete(pm.parentConstraint(obj,grp))
        pm.parent(obj,grp)
        return grp
    except:
        print (obj+' Zero Out failed')

def RevGroup(obj):
    try:
        parent = pm.listRelatives(obj,p=1)
        grp = pm.createNode('transform',n = obj + '_Rev_Group')
        pm.delete(pm.parentConstraint(obj,grp))
        pm.parent(obj,grp)
        MD = pm.createNode('multiplyDivide', n = obj+'_MD')
        pm.parent(grp,parent)
        obj.t>>MD.input1
        MD.output>>grp.t
        MD.input2.set(-1,-1,-1)

        return grp
    except:
        print (obj+' Zero Out failed')


sel = pm.ls(sl=1)

if len(sel)== 2:
    print(sel[0]+ ' is the Parent & '+sel[1]+'is the Child ')

    Parent = sel[0]
    Child = sel[1]
    ChildParent = pm.listRelatives(Child,p=1)
    print (ChildParent)


else:
    print('Please Select 2 transforms Parent than child')    
    
