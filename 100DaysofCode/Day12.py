import maya.OpenMaya as om
import maya.OpenMayaMPx as omMPx
import random
#Set name and id
nodeName = 'jitter'
nodeId = om.MTypeId(0x101213)


#jit node - uses mpxnode as base
class jitterNode(omMPx.MPxNode):
    #input and output vars

    INPUT = om.MObject()
    OUTPUT = om.MObject()

    def __init__(self):
        omMPx.MPxNode.__init__(self)
    
    def compute(self,plug,datablock):
        if (plug == jitterNode.OUTPUT):
            dataHandle = datablock.inputValue(jitterNode.INPUT)
            inFloat = dataHandle.asFloat()
            result = random.uniform(-1,1)+inFloat
            outputHandle = datablock.outputValue(jitterNode.OUTPUT)
            outputHandle.setFloat(result)
            datablock.setClean(plug)






def nodeCreator():
    #Creating jitterNode
    return omMPx.asMPxPtr(jitterNode())

def nodeInit():
    #init me
    numAttr = om.MFnNumericAttribute()
    jitterNode.INPUT= numAttr.create('input','in',om.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)

    numAttr = om.MFnNumericAttribute()
    jitterNode.OUTPUT = numAttr.create('output','out',om.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)
    numAttr.setWritable(1)


    jitterNode.addAttribute(jitterNode.INPUT)
    jitterNode.addAttribute(jitterNode.OUTPUT)
    jitterNode.attributeAffects(jitterNode.INPUT,jitterNode.OUTPUT)




# This is used for loading plugins
def initializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(nodeName, nodeId, nodeCreator, nodeInit)
    except:
        sys.stderr.write("Error loading")
        raise

# This is used for removing plugins
def uninitializePlugin(mobject):
    mplugin = omMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode( nodeId )
    except:
        sys.stderr.write("Error removing")
        raise
