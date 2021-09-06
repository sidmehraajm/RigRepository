#module for making Rig structure
import maya.cmds as cmds
from . import ControlCode
sceneObjectType = 'Rig'
class FirstBase():
	

	

	#Class for building Rig Base





	def __init__(self,characterName='Name',scale=1.0):
		self.topGroup = cmds.group(n=characterName+'_World',em=1)
		self.rigGroup = cmds.group(n=characterName+'_Rig_Group',em=1,p=self.topGroup )
		self.geoGroup = cmds.group(n=characterName+'_Geo_Group',em=1,p=self.topGroup)

		characterNameAt = 'characterName'
		sceneObjectTypeAt = 'sceneObjectTypeAt'

		for at in[characterNameAt,sceneObjectTypeAt]:
			cmds.addAttr(self.topGroup,ln=at,dt='string')


		cmds.setAttr(self.topGroup+'.'+characterNameAt,characterName,type = 'string',l=1)
		cmds.setAttr(self.topGroup+'.'+sceneObjectTypeAt,sceneObjectType,type = 'string',l=1)


		#make global control


		globalCtrl01 =  ControlCode.Ctl(prefix = 'Global_01',scale =scale*3.5,parentTo = self.rigGroup ,lockCh=['v'],ctrlNormal=[0,1,0])
		globalCtrl02 =  ControlCode.Ctl(prefix = 'Global_02',scale =scale*4,parentTo = globalCtrl01.C ,lockCh=['s','v'],ctrlNormal=[0,1,0])
		cmds.addAttr(globalCtrl01.C,ln='GlobalScale',at='double',min=0.0,k=1 ,dv=1.0)
		


		for axis in ['x','y','z']:

			cmds.connectAttr(globalCtrl01.C+'.GlobalScale',globalCtrl01.C+'.s'+axis)
			cmds.setAttr(globalCtrl01.C+'.s'+axis,k=0)


		#make extra groups

		self.jointsGrp = cmds.group(n='JointsGrp',em=1,p=globalCtrl02.C)
		self.ModuleGrp = cmds.group(n='SetupModules_Grp',em=1,p=globalCtrl02.C)

		self.partGrp = cmds.group(n='Parts(Static)_Grp',em=1,p=self.rigGroup)

		cmds.setAttr(self.partGrp+'.it',0,l=1)



#################################################################################################


class Mod():
	

	

	#Class for Rig Module 





	def __init__(self,prefix='Name',baseObj = None):
		self.topGroup = cmds.group(n=prefix+'_ModuleGrp',em=1)
		self.ControlGroup = cmds.group(n=prefix+'_CtrlGrp',em=1)
		self.JointsGroup = cmds.group(n=prefix+'JntGrp',em=1)
		self.PartsGroup = cmds.group(n=prefix+'_PartsGrp',em=1)

		self.partnoTransGrp = cmds.group(n=prefix+'_Part(NoTrans)_Grp',em=1)
		cmds.setAttr(self.partnoTransGrp+'.it',0,l=1)







