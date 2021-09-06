#Matrix Constraints works only when the target object has a upper group/parent

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

def ParentScaleConstraintMtx(obj1,obj2):

    sel = [obj1,obj2]

    if len(sel)== 2:
        print(sel[0]+ ' is the Parent & '+sel[1]+'is the Child ')

        Parent = sel[0]
        Child = sel[1]
        ChildParent = pm.listRelatives(Child,p=1)[0]
        print (ChildParent)
        MainMultMatx = pm.createNode('multMatrix',n= (Parent+'_Con_Matrix'))
        TempMultMatx = pm.createNode('multMatrix')
        DCM = pm.createNode('decomposeMatrix',n= (Parent+'_DCM'))
        Parent.worldMatrix[0]>>MainMultMatx.matrixIn[1]
        ChildParent.worldInverseMatrix[0]>>MainMultMatx.matrixIn[2]
        Child.worldMatrix[0]>>TempMultMatx.matrixIn[0]
        Parent.worldInverseMatrix[0]>>TempMultMatx.matrixIn[1]
        OfffMarixValue = TempMultMatx.matrixSum.get()
        MainMultMatx.matrixIn[0].set(OfffMarixValue)
        MainMultMatx.matrixSum>>DCM.inputMatrix
        DCM.outputTranslate>>Child.translate
        DCM.outputRotate>>Child.rotate
        DCM.outputScale>>Child.scale

    else:
        print('Please Select 2 transforms Parent than child')    



def RotationConstraintMtx(obj1,obj2):
    '''
    Works like Orient Con
    '''
    
    sel = [obj1,obj2]

    if len(sel)== 2:
        print(sel[0]+ ' is the Parent & '+sel[1]+'is the Child ')

        Parent = sel[0]
        Child = sel[1]
        ChildParent = pm.listRelatives(Child,p=1)[0]
        print (ChildParent)
        MainMultMatx = pm.createNode('multMatrix',n= (Parent+'_Con_Matrix'))
        TempMultMatx = pm.createNode('multMatrix')
        DCM = pm.createNode('decomposeMatrix',n= (Parent+'_DCM'))
        Parent.worldMatrix[0]>>MainMultMatx.matrixIn[1]
        ChildParent.worldInverseMatrix[0]>>MainMultMatx.matrixIn[2]
        Child.worldMatrix[0]>>TempMultMatx.matrixIn[0]
        Parent.worldInverseMatrix[0]>>TempMultMatx.matrixIn[1]
        OfffMarixValue = TempMultMatx.matrixSum.get()
        MainMultMatx.matrixIn[0].set(OfffMarixValue)
        MainMultMatx.matrixSum>>DCM.inputMatrix
        DCM.outputRotate>>Child.rotate


    else:
        print('Please Select 2 transforms Parent than child')    

def ScaleConstraintMtx(obj1,obj2):
    
    sel = [obj1,obj2]

    if len(sel)== 2:
        print(sel[0]+ ' is the Parent & '+sel[1]+'is the Child ')

        Parent = sel[0]
        Child = sel[1]
        ChildParent = pm.listRelatives(Child,p=1)[0]
        print (ChildParent)
        MainMultMatx = pm.createNode('multMatrix',n= (Parent+'_Con_Matrix'))
        TempMultMatx = pm.createNode('multMatrix')
        DCM = pm.createNode('decomposeMatrix',n= (Parent+'_DCM'))
        Parent.worldMatrix[0]>>MainMultMatx.matrixIn[1]
        ChildParent.worldInverseMatrix[0]>>MainMultMatx.matrixIn[2]
        Child.worldMatrix[0]>>TempMultMatx.matrixIn[0]
        Parent.worldInverseMatrix[0]>>TempMultMatx.matrixIn[1]
        OfffMarixValue = TempMultMatx.matrixSum.get()
        MainMultMatx.matrixIn[0].set(OfffMarixValue)
        MainMultMatx.matrixSum>>DCM.inputMatrix
        DCM.outputScale>>Child.scale


    else:
        print('Please Select 2 transforms Parent than child')    


def ParentConstraintMtx(obj1,obj2):

    sel = [obj1,obj2]

    if len(sel)== 2:
        print(sel[0]+ ' is the Parent & '+sel[1]+'is the Child ')

        Parent = sel[0]
        Child = sel[1]
        ChildParent = pm.listRelatives(Child,p=1)[0]
        print (ChildParent)
        MainMultMatx = pm.createNode('multMatrix',n= (Parent+'_Con_Matrix'))
        TempMultMatx = pm.createNode('multMatrix')
        DCM = pm.createNode('decomposeMatrix',n= (Parent+'_DCM'))
        Parent.worldMatrix[0]>>MainMultMatx.matrixIn[1]
        ChildParent.worldInverseMatrix[0]>>MainMultMatx.matrixIn[2]
        Child.worldMatrix[0]>>TempMultMatx.matrixIn[0]
        Parent.worldInverseMatrix[0]>>TempMultMatx.matrixIn[1]
        OfffMarixValue = TempMultMatx.matrixSum.get()
        MainMultMatx.matrixIn[0].set(OfffMarixValue)
        MainMultMatx.matrixSum>>DCM.inputMatrix
        DCM.outputTranslate>>Child.translate
        DCM.outputRotate>>Child.rotate

    else:
        print('Please Select 2 transforms Parent than child')    
