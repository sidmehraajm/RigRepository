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

wind = pm.window( 'TheRiggersToolkitX',t = 'RigToolkitX',w=300,h=330,s=1,bgc = [(.17),(.18),(.19)])
Tab = tabLayout('Tabs',p='TheRiggersToolkitX',tc =1,stb=1,snt=1,ntc = 'NewTab()')

ToolsSc = pm.scrollLayout('Controls',p='Tabs',w=300,h=350)
ToolsSc = pm.scrollLayout('Tools',p='Tabs')
channelbox = pm.channelBox('ChannelBox',p = 'Tabs',ac = [(.8),(.9),(1)],bc = [(.3),(.3),(.3)],fw=150,hlc=[(.2),(.6),(.4)],hol =1,ln=1,nn=0,m=1,pre = 5,)
out = pm.formLayout('Outliner',p='Tabs',w=300,h=330)
outpanel = pm.outlinerPanel(p = 'Outliner')


SkinSc= pm.scrollLayout('Skin',p='Tabs')
ScriptEdt = pm.scrollLayout('MelCmd',p='Tabs')
MiscSc = pm.scrollLayout('Misc',p='Tabs')


cmdShll = cmds.cmdShell(p='MelCmd',w=295,h=302 , bgc = [(.17),(.18),(.19)])
clearBtn = pm.symbolButton('minusBtn',p = 'MelCmd',i = 'clearAll.png',w = 295,h=43,ebg =1 , bgc = [(.1),(.11),(.11)],en = 1,command=('cmds.cmdShell(\"' + cmdShll + '\", edit=True, clear=True)' ))


ControlsForm = pm.formLayout( 'ControlsForm',p='Controls')

ToolsForm = pm.formLayout('ToolkitForm',p='Tools')
SkinForm = pm.formLayout('SkinForm',p='Skin')
MiscForm = pm.formLayout('MiscForm',p='Misc')

GlobalName = pm.textField('Globalfield', w = 270 , h=25 ,pht = 'Name for Ctrls or Attrs',p = 'ControlsForm',bgc = [(.17),(.18),(.19)])

BaseCtlBtn = pm.iconTextButton('ControlBase',style='iconAndTextHorizontal', image1='polyColorSetEditor.png', label='Control Class',p = 'ControlsForm',w=130,h=40, bgc = [(.3),(.5),(.5)])
BaseCtlShapeBtn = pm.iconTextButton('ControlShape',style='iconAndTextHorizontal', image1='fluidCreate3D.png', label='Control Shape',p = 'ControlsForm',w=130,h=40,  bgc = [(.3),(.5),(.5)])
Border01Btn = pm.button('Border01',l = '',p = 'ControlsForm',w= 260,h = 60,en=0)

CtrlSizeText = pm.iconTextButton('Sizetxt',style='iconAndTextHorizontal',image1='StandinShelf.png',l = 'SHAPE SIZE',p = 'ControlsForm',w = 105,h=40, bgc = [(.2),(.3),(.3)],en = 1)
intensityTxtFld = pm.floatField('intenTxf',min = .10,p = 'ControlsForm',v=.10,w= 45,h =40,bgc = [(.17),(.18),(.19)] )
plusBtn = pm.symbolButton('plusBtn',p = 'ControlsForm',i = 'UVTBAdd.png',w = 40,h=40,ebg =1 , bgc = [(.2),(.3),(.3)],en = 1,c='ScalePlus()')
minusBtn = pm.symbolButton('minusBtn',p = 'ControlsForm',i = 'UVTBRemove.png',w = 40,h=40,ebg =1 , bgc = [(.2),(.3),(.3)],en = 1,c='ScaleMinus()')


attrsBtn = pm.button('atrBtn',l= 'Attributes',p = 'ControlsForm',w = 270,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)



lockatBtn = pm.symbolButton('lockatrBtn',p = 'ControlsForm',i = 'Lock_ON.png',w = 63,h=25,ebg =1 , bgc = [(.3),(.2),(.2)],en = 1)
unlockatBtn = pm.symbolButton('unlockatrBtn',p = 'ControlsForm',i = 'Lock_OFF.png',w = 63,h=25,ebg =1 , bgc = [(.3),(.2),(.2)],en = 1)
keyableBtn = pm.symbolButton('keyableAtBtn',p = 'ControlsForm',i = 'keyIntoclip.png',w = 63,h=25,ebg =1 , bgc = [(.3),(.2),(.2)],en = 1)
hideBtn = pm.symbolButton('hideAtBtn',p = 'ControlsForm',i = 'RS_visible.png',w = 63,h=25,ebg =1 , bgc = [(.3),(.2),(.2)],en = 1)

OnOffAttr = pm.button('OnOff',l= 'Off/On',p = 'ControlsForm',w = 63,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)
ZeroOneAttr = pm.button('ZeroOneAtr',l= '0.0-1.0',p = 'ControlsForm',w = 63,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)
ZeroTenAttr = pm.button('ZeroTenAtr',l= '0-10',p = 'ControlsForm',w = 63,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)
IntAttr= pm.button('IntAtr',l= '0-1',p = 'ControlsForm',w = 63,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)

EnumAttrBtn= pm.button('EnumAtr',l= 'Enum',p = 'ControlsForm',w = 132,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)
StringAttrBtn= pm.button('StringAtr',l= 'String',p = 'ControlsForm',w = 132,h=19, bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1)
JntCreate= pm.iconTextButton('CreateJnt',style='iconAndTextHorizontal',image1='CenterPivot.png',l = 'Create Joint CTR ',p = 'ControlsForm',w = 132,h=40, bgc = [(.2),(.3),(.3)],en = 1,c = 'CtrJnt()')
EachJntCreate= pm.iconTextButton('EachCreateJnt',style='iconAndTextHorizontal',image1='out_particle.png',l = 'Create Joint Each',p = 'ControlsForm',w = 132,h=40, bgc = [(.2),(.3),(.3)],en = 1,c = 'CtrJntEach()')

outliner = pm.outlinerPanel(outpanel, query=True,outlinerEditor=True)

pm.outlinerEditor( outliner, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showNamespace=True, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter' )


pm.formLayout('Outliner',e =1,af=[(outpanel,'top',0),(outpanel,'left',0),(outpanel,'right',0),(outpanel,'bottom',0)])
pm.formLayout('ControlsForm',e=1,
	attachForm = [
	
	
	(GlobalName,'top',8),
	(BaseCtlBtn,'top',45),
	(BaseCtlShapeBtn,'top',45),
	
	(Border01Btn,'right',10),
	(BaseCtlShapeBtn,'right',10),


	
	(GlobalName,'left',10),
	(BaseCtlBtn,'left',10),
	(CtrlSizeText,'left',20),
	(Border01Btn,'left',10),
	(lockatBtn,'left',10),
	(attrsBtn,'left',10),	
	(OnOffAttr,'left',10),	
	(EnumAttrBtn,'left',10),	
	(JntCreate,'left',10),	
	(EachJntCreate,'left',10),		
	
	],
	attachControl = [
	
	(BaseCtlShapeBtn, 'left' , 10 , BaseCtlBtn ),

	(plusBtn, 'left' , 6 , CtrlSizeText ),
	(intensityTxtFld, 'left' , 6 , plusBtn ),
	(minusBtn, 'left' , 6 , intensityTxtFld ),
	(attrsBtn, 'top' , 12 , Border01Btn ),
	(unlockatBtn, 'left' , 6 , lockatBtn ),
	(keyableBtn, 'left' , 6 , unlockatBtn ),
	(hideBtn, 'left' , 6 , keyableBtn ),
	(ZeroOneAttr, 'left' , 6 , OnOffAttr ),
	(ZeroTenAttr, 'left' , 6 , ZeroOneAttr ),
	(IntAttr, 'left' , 6 , ZeroTenAttr ),
	(StringAttrBtn, 'left' , 6 , EnumAttrBtn ),
	(EachJntCreate, 'left' , 6 , JntCreate ),
	
		
	(intensityTxtFld, 'top' , 18 , BaseCtlShapeBtn ),
	(Border01Btn, 'top' , 10 , BaseCtlShapeBtn ),
	(CtrlSizeText, 'top' , 18 , BaseCtlShapeBtn ),
	(plusBtn, 'top' , 18 , BaseCtlShapeBtn ),
	(minusBtn, 'top' , 18 , BaseCtlShapeBtn ),
	(unlockatBtn, 'top' , 10 , attrsBtn ),
	(lockatBtn, 'top' , 10 , attrsBtn ),
	(keyableBtn, 'top' , 10 , attrsBtn ),	
	(hideBtn, 'top' , 10 , attrsBtn ),
	(OnOffAttr, 'top' , 10 , hideBtn ),
	(ZeroOneAttr, 'top' , 10 , hideBtn ),
	(ZeroTenAttr, 'top' , 10 , hideBtn ),
	(IntAttr, 'top' , 10 , hideBtn ),
	(EnumAttrBtn, 'top' , 10 , IntAttr ),
	(StringAttrBtn, 'top' , 10 , IntAttr ),
	(JntCreate, 'top' , 10 , StringAttrBtn ),
	(EachJntCreate, 'top' , 10 , StringAttrBtn ),
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
    
	pm.menuItem(p=CtlMenu, l="Ctrl At Each Piv", rp="SW", c="print 'SouthWest'")
	pm.menuItem(p=CtlMenu, l="Ctrl At Ctr", rp="NE", c="pm.circle(n = 'pSolid_Ctrl')")
	


Control_MM_UI()

def NewTab():
    pm.scrollField( 'Notes',p = 'Tabs', bgc = [(.2),(.2),(.2)],hlc = [(.9),(.2),(.2)],en =1 )
    Tab = tabLayout('Tabs',e =1 , snt=0)
    
    
    
    
 
def CtrJnt():
    #createJoint

    sl = pm.ls(sl=1)
    try:
        pm.select(sl)
        tempPos = pm.cluster(n='Temp')[1]
        Jnt = pm.createNode('joint',n = (sl[0]+'Jnt'))
        pm.delete(pm.parentConstraint(tempPos,Jnt))
        pm.delete(tempPos)
        
        
        
        
    except:
        tempPos = pm.createNode('transform',n = 'Temp')
        pm.delete(pm.parentConstraint(sl,tempPos))
        Jnt = pm.createNode('joint',n = (sl[0]+'_Jnt'))
        pm.delete(pm.parentConstraint(tempPos,Jnt))
        pm.delete(tempPos)
        
        
        
    
    

def CtrJntEach():
    
    #createJoint
    try:sl = getSelection()
    except:sl= pm.ls(sl=1)
    for i in sl:
        
        
        try:
            pm.select(i)
            tempPos = pm.cluster(n='Temp')[1]
            Jnt = pm.createNode('joint',n = (i+'Jnt'))
            pm.delete(pm.parentConstraint(tempPos,Jnt))
            pm.delete(tempPos)
            
            
            
            
        except:
            tempPos = pm.createNode('transform',n = 'Temp')
            pm.delete(pm.parentConstraint(i,tempPos))
            Jnt = pm.createNode('joint',n = (i+'_Jnt'))
            pm.delete(pm.parentConstraint(tempPos,Jnt))
            pm.delete(tempPos)
            
        
        
def getSelection():
    components = cmds.ls(sl=1)
    selList = []
    objName = components[0][0:components[0].index(".")]
    # go through every component in the list. If it is a single component ("pCube1.vtx[1]"), add it to the list. Else,
    # add each component in the index ("pCube1.vtx[1:5]") to the list
    for c in components:
        if ":" not in c:
            selList.append(c)
        else:
            print c
            startComponent = int(c[c.index("[") + 1: c.index(":")])
            endComponent = int(c[c.index(":") + 1:c.index("]")])
            componentType = c[c.index(".") + 1:c.index("[")]
            while startComponent <= endComponent:
                selList.append(objName + "." + componentType + "[" + str(startComponent) + "]")
                startComponent += 1

    return selList
    
def ScalePlus(): 
    v = 1.1
    
    b = pm.ls(sl=True)[0]
    
    a = pm.listRelatives(b,s=1)
    TmpTrans = []
    newShp = []
    
    for i in a:
    	tmtr  = pm.createNode('transform',n=('temp'+i))
    	pm.parent(i,tmtr,r =True, s = True)
    	
    	#nshape = pm.duplicate(i,n=('temp'+i))
    	pm.xform(tmtr,s=(v,v,v))
    	pm.makeIdentity(tmtr, apply=True, t=1, r=1, s=1 )
    	newShp.append(i)
    	TmpTrans.append(tmtr)
    	
    pm.select(cl=True)
    
    
    
    for i in newShp:
    	pm.select(i)
    	pm.rename(i,b+'_Shape_00')
    	pm.select(b , add=True)
    	pm.parent(r=True,s=True)
    pm.delete(TmpTrans)
    pm.select(b)
    
def ScaleMinus(): 
    v = .9
    
    b = pm.ls(sl=True)[0]
    
    a = pm.listRelatives(b,s=1)
    TmpTrans = []
    newShp = []
    
    for i in a:
    	tmtr  = pm.createNode('transform',n=('temp'+i))
    	pm.parent(i,tmtr,r =True, s = True)
    	
    	#nshape = pm.duplicate(i,n=('temp'+i))
    	pm.xform(tmtr,s=(v,v,v))
    	pm.makeIdentity(tmtr, apply=True, t=1, r=1, s=1 )
    	newShp.append(i)
    	TmpTrans.append(tmtr)
    	
    pm.select(cl=True)
    
    
    
    for i in newShp:
    	pm.select(i)
    	pm.rename(i,b+'_Shape_00')
    	pm.select(b , add=True)
    	pm.parent(r=True,s=True)
    pm.delete(TmpTrans)
    pm.select(b) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
