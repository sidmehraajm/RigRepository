import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omR
import maya.cmds as cmds


def maya_useNewAPI():
    pass

class HelloWorldNode(omui.MPxLocatorNode):
    TypeName = "Krishna"
    TypeID = om.MTypeId(0x0007F7F9)

    
    def __init__(self):
        super(HelloWorldNode, self).__init__()

    @classmethod
    def creator(cls):
        return HelloWorldNode()
    @classmethod
    def initialize():
        pass




def initializePlugin(plugin):

    vendor = "Chris Zurbrigg"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)
    try:
        pluginFn.registerNode(HelloWorldNode.TypeName,
                             HelloWorldNode.TypeID,
                             HelloWorldNode.creator,
                             HelloWorldNode.initialize)
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





