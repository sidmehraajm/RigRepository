import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omR
import maya.cmds as cmds


def maya_useNewAPI():
    pass

class HelloWorldNode(omui.MPxLocatorNode):
    TypeName = "Krishna"
    TypeID = om.MTypeId(0x0007F7F7)
    DrawClassification = 'drawdb/geometry/hello'
    DrawRegID = 'HelloWorldNode'
    def __init__(self):
        super(HelloWorldNode, self).__init__()

    @classmethod
    def creator(cls):
        return HelloWorldNode()
    @classmethod
    def initialize():
        pass

class HelloWorldDrawovd(omR.MPxDrawOverride):
    Name = 'DrawOvd'
    def __init__(self,obj):
        super(HelloWorldDrawovd, self).__init__(obj,None,False)

    def Drawing(self,obj_path,camera_path,frame_context,old_data):
        pass

    def supportedDrawAPIs(self):
        return (omR.MRenderer.kAllDevices)

    def hasUIDrawables(self):
        return True
    
    def addUIDrawables(self,obj_path,draw_manager,frame_context,data):
        draw_manager.beginDrawable()
        draw_manager.text2d(om.MPoint(100,200),'Hare Krishna')
        draw_manager.endDrawable()
    
    @classmethod
    def creator(cls,obj):
        return HelloWorldDrawovd(obj)






def initializePlugin(plugin):

    vendor = "Chris Zurbrigg"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)
    try:
        pluginFn.registerNode(HelloWorldNode.TypeName,
                             HelloWorldNode.TypeID,
                             HelloWorldNode.creator,
                             HelloWorldNode.initialize,
                             om.MPxNode.kLocatorNode,
                             HelloWorldNode.DrawClassification)
        print ("Command initialized")
    except:
        om.MGlobal.displayError("Failed to regiser Command")

    try:
        omR.MDrawRegistry.registerDrawOverrideCreator(HelloWorldNode.DrawClassification,
                                                      HelloWorldNode.DrawRegID,
                                                      HelloWorldDrawovd.creator)

    except:
        om.MGlobal.displayError("Failed to regiser Command")
        


def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    
    
    try:
        omR.MDrawRegistry.deRegisterDrawOverrideCreator(HelloWorldNode.DrawClassification,HelloWorldNode.DrawRegID)
        
    except:
        om.MGlobal.displayError("Failed to De-regiser Command:")

    try:
        pluginFn.deregisterNode(HelloWorldNode.TypeID)
        print ("Command uninitialized")
        
    except:
        om.MGlobal.displayError("Failed to De-regiser Command:")





