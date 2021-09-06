'''
Control Module
For Rig Controls
 '''

import pymel.core as pm
from maya import cmds 


class Ctl():

#class for building Rig Controls

    def __init__(self,prefix = 'Temp',scale = 1.0,translateTo = '',rotateTo = '',shape='',CtlParent = '',lockChannels = ['v','s'],color = 'blue'):

                
        ctrl = cmds.circle(n = prefix + '_Ctrl',ch=0,nr=[1,0,0],r = scale)[0]
        OffGroup = cmds.group(ctrl,n=prefix + '_Ctrl_Group')

        #translate Control

        if cmds.objExists(translateTo):
            try:
                cmds.pointConstraint(translateTo,OffGroup)

            except:
                print 'Unable to Move control to given translate object'

        #Rotate Control

        if cmds.objExists(rotateTo):
            try:
                cmds.orientConstraint(translateTo,OffGroup)

            except:
                print 'Unable to Rotate control to given rotate object'


        #Control Parent

        if cmds.objExists(CtlParent):
            try:

                cmds.parent(OffGroup,CtlParent)

            except:
                print 'Unable to Parent control to given Parent object'

        #Locking chanells 
        singleAttrLockList = []


        for lockChannels in lockChannels:
            if lockChannels in ['t','r','s']:
                for axis in ['x','y','z']:
                    at = lockChannels+axis
                    singleAttrLockList.append(at)



            else:
                singleAttrLockList.append(lockChannels)




        for at in singleAttrLockList:
            try:
                cmds.setAttr(ctrl+'.'+at,l=True,k=0)
            except:
                print('Unable to lock'+ctrl+'.'+at)


        #Color
        if cmds.objExists(color):
            cmds.circle()
            print 'yeah'
            if color == 'blue':
                cmds.circle()
                print 'blue color'
            elif color == 'red':
                cmds.circle()
                print 'red'

            else:
                print 'ok'


		#controlColor
		ctrlShape = cmds.listRelatives(ctrl,s=True)
		[cmds.setAttr(i+'.ove',1)for i in ctrlShape]
		if prefix.startswith('LT_'):
			for s in ctrlShape:
				cmds.setAttr( s + '.ovc',20 )	
			print 'ltColor'
		elif prefix.startswith('RT_'):
			 for s in ctrlShape:
			 	cmds.setAttr( s + '.ovc', 13 )
		else:
			 for s in ctrlShape:
			 	cmds.setAttr( s + '.ovc', 22 )











        # Add Public Members
        self.C = ctrl
        self.Off = OffGroup











            

















  





















