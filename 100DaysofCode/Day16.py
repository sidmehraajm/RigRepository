import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omR
import maya.cmds as cmds


def maya_useNewAPI():
    pass

class HelloWorldNode(omui.MPxLocatorNode):
    TypeName = "Krishna"
    TypeID = om.MTypeId(0x00307f7f9)
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
    def __init__(self):
        super(HelloWorldDrawovd, self).__init__(obj,None,False)

    def Drawing(self,obj_path,camera_path,frame_context,old_data):
        pass

    def supportedDrawAPIs(self):
        omR.MRenderer.kAllDevices

    def hasUIDrawables(self):
        return True
    
    def addUIDrawables(self,obj_path,draw_manager,frame_context,data)




def initializePlugin(plugin):

    vendor = "Chris Zurbrigg"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)
    try:
        pluginFn.registerNode(HelloWorldNode.TypeName,
                             HelloWorldNode.TypeID,
                             HelloWorldNode.creator,
                             HelloWorldNode.initialize,
                             om.MPxNode.kLocatorNode                             
                             )
        print ("Command initialized")
    except:
        om.MGlobal.displayError("Failed to regiser Command")

def uninitializePlugin(plugin):

    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(HelloWorldNode.TypeID)
        print ("Command uninitialized")
    except:
        om.MGlobal.displayError("Failed to De-regiser Command:")




