import pymel.core as pm
from pymel.core import *

if window('TheRiggersToolkitX',ex=True):
	deleteUI('TheRiggersToolkitX')
if window('ExamplaeWindow',ex=True):
	deleteUI('ExamplaeWindow')

if cmds.windowPref('TheRiggersToolkitX', exists=True ):
   cmds.windowPref( 'TheRiggersToolkitX', r=1 )
	
template = uiTemplate('TheRiggersToolkitXtemplate', force=True)
template.define(formLayout)

wind = pm.window( 'TheRiggersToolkitX',t = 'RigToolkitX',w=300,h=300,s=0,bgc = [(.17),(.18),(.19)])
Tab = tabLayout('Tabs',p='TheRiggersToolkitX')



ToolsSc = pm.scrollLayout('Controls',p='Tabs')

ToolsSc = pm.scrollLayout('Tools',p='Tabs')
SkinSc= pm.scrollLayout('Skin',p='Tabs')
MiscSc = pm.scrollLayout('Misc',p='Tabs')

ControlsForm = pm.formLayout( 'ControlsForm',p='Controls')

ToolsForm = pm.formLayout('ToolkitForm',p='Tools')
SkinForm = pm.formLayout('SkinForm',p='Skin')
MiscForm = pm.formLayout('MiscForm',p='Misc')

BaseCtlBtn = pm.iconTextButton('ControlBase',style='iconAndTextHorizontal', image1='polyColorSetEditor.png', label='Control Class',p = 'ControlsForm',w=130,h=40, bgc = [(.3),(.5),(.5)])
BaseCtlShapeBtn = pm.iconTextButton('ControlShape',style='iconAndTextHorizontal', image1='fluidCreate3D.png', label='Control Shape',p = 'ControlsForm',w=130,h=40, bgc = [(.2),(.3),(.3)])
Border01Btn = pm.button('Border01',l = '',p = 'ControlsForm',w= 260,h = 60,en=0)

CtrlSizeText = pm.iconTextButton('Sizetxt',style='iconAndTextHorizontal',image1='StandinShelf.png',l = 'SHAPE SIZE',p = 'ControlsForm',w = 105,h=40, bgc = [(.2),(.3),(.3)],en = 1)
intensityTxtFld = pm.floatField('intenTxf',min = .10,p = 'ControlsForm',v=.10,w= 45,h =40,bgc = [(.17),(.18),(.19)] )
plusBtn = pm.symbolButton('plusBtn',p = 'ControlsForm',i = 'UVTBAdd.png',w = 40,h=40,ebg =1 , bgc = [(.2),(.3),(.3)],en = 1)
minusBtn = pm.symbolButton('minusBtn',p = 'ControlsForm',i = 'UVTBRemove.png',w = 40,h=40,ebg =1 , bgc = [(.2),(.3),(.3)],en = 1)

pm.formLayout('ControlsForm',e=1,
	attachForm = [
	(BaseCtlBtn,'top',10),
	(BaseCtlShapeBtn,'top',10),
	
	
	(BaseCtlBtn,'left',10),
	(CtrlSizeText,'left',20),
	
	(Border01Btn,'left',10),
	(Border01Btn,'right',10),
	(BaseCtlShapeBtn,'right',10)
	
	],
	attachControl = [
	
	(BaseCtlShapeBtn, 'left' , 10 , BaseCtlBtn ),

	(plusBtn, 'left' , 6 , CtrlSizeText ),
	(intensityTxtFld, 'left' , 6 , plusBtn ),
	(minusBtn, 'left' , 6 , intensityTxtFld ),
	
	(intensityTxtFld, 'top' , 18 , BaseCtlShapeBtn ),
	(Border01Btn, 'top' , 10 , BaseCtlShapeBtn ),
	(CtrlSizeText, 'top' , 18 , BaseCtlShapeBtn ),
	(plusBtn, 'top' , 18 , BaseCtlShapeBtn ),
	(minusBtn, 'top' , 18 , BaseCtlShapeBtn ),
	
	]
	
	
	
	
	
	)


with wind:
	with template:
		with Tab:
			print 'Launching ToolkitX'
			


















def Control_MM_UI():
	
	if pm.popupMenu('ControlMenu', ex=1):
		pm.deleteUI('ControlMenu')
    	
	
	CtlMenu = pm.popupMenu('ControlMenu', mm=1, b=(1), aob=1, ctl=0, alt=0, sh=0, p="ControlBase", pmo=1)
    
	pm.menuItem(p=CtlMenu, l="Print Fn", rp="SW", c="print 'SouthWest'")
	pm.menuItem(p=CtlMenu, l="Circle", rp="NE", c="pm.circle()")
	


Control_MM_UI()


