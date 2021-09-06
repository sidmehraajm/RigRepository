import maya.api.OpenMaya as om
import maya.cmds as cmds


def maya_useNewAPI():
    pass

class HelloWorldCommand(om.MPxCommand):
    CName = 'HareKrishna'
    
    def __init__(self):
        super(HelloWorldCommand, self).__init__()

    def doIt(self,args):
        print ("Hare Krishna")
    
    @classmethod
    def creator(cls):
        return HelloWorldCommand()

    




def initializePlugin(plugin):

    vendor = "Chris Zurbrigg"
    version = "1.0.0"

    pluginFn = om.MFnPlugin(plugin, vendor, version)
    try:
        pluginFn.registerCommand(HelloWorldCommand.CName, HelloWorldCommand.creator)
        print ("Command initialized")
    except:
        om.MGlobal.displayError("Failed to regiser Command")

def uninitializePlugin(plugin):

    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(HelloWorldCommand.CName)
        print ("Command uninitialized")
    except:
        om.MGlobal.displayError("Failed to De-regiser Command:")




