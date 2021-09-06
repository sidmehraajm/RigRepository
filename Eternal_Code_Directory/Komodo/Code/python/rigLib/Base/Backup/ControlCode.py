'''
module for making Rig Controls
'''
import maya.cmds as cmds
class Ctl():
	

	"""Class for building controls"""





	def __init__(self,	prefix = 'Test',scale =1.0,transTo='',rotateTo='',	parentTo = '',lockCh=['s','v'],ctrlNormal=[1,0,0]):


		ctrlobj = cmds.circle(n=(prefix+'_Ctrl'),ch=False,normal = ctrlNormal,radius = scale     )[0]
		ctrlOffset = cmds.group(ctrlobj,n = (prefix+'_Off_Group'),em=1)
		cmds.parent(ctrlobj,ctrlOffset)
		
		#controlColor
		ctrlShape = cmds.listRelatives(ctrlobj,s=True)
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





		# translate control
		if cmds.objExists(transTo):
			cmds.delete(cmds.pointConstraint(transTo,ctrlOffset))

        # rotate control

		if cmds.objExists(rotateTo):
			cmds.delete(cmds.orientConstraint(transTo,ctrlOffset))
        # parent control

		if cmds.objExists(parentTo):
			cmds.parent(ctrlOffset,parentTo)



        # lock control channels

		singleAttrLockList=[]
		for lockChanel in lockCh:
			if lockChanel in ['t','r','s']:
				for axis in ['x','y','z']:
					at = lockChanel+axis
					singleAttrLockList.append(at)

			else:
				singleAttrLockList.append(lockChanel)


		for at in singleAttrLockList:
			cmds.setAttr(ctrlobj+'.'+at,l=1,k=0)




        # add public members

		self.C = ctrlobj
		self.Off = ctrlOffset

	


















