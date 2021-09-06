import math, sys
    
import maya.OpenMaya as om
import maya.OpenMayaMPx as omx

kPluginNodeTypeName = "AutoWheel"
kPluginNodeId = om.MTypeId(0x87055)

#Node
class Wheel(omx.MPxNode):
    #vars
    aInput = om.MObject()
    bInput = om.MObject()
    aOutput = om.MObject()

    def __init__(self):
        omx.MPxNode.__init__(self)


    def compute(self,plug,data):
        if(plug == Wheel.aOutput):
            inputTransform = data.inputValue(Wheel.aInput)
            axis = data.inputValue(Wheel.bInput)
            print(inputTransform,axis)
            result = 10
            a = data.outputValue(Wheel.aOutput)
            a.setFloat(result)
            data.setClean(plug)
        else:
            print('Hey')


def nodeCreator():
    return omx.asMPxPtr(Wheel())

def nodeInitializer():
    nAttr = om.MFnNumericAttribute()

    Wheel.aInput = nAttr.create("Transform", "in", om.MFnNumericData.kFloat, 0.0)
    nAttr.setStorable(True)
    Wheel.bInput = nAttr.create("TransformDirection", "id", om.MFnNumericData.kVectorArray, [0.0,0.0,0.0])
    nAttr.setStorable(True)
    Wheel.aOutput = nAttr.create("sineOutput", "so", om.MFnNumericData.kFloat, 0.0)
    nAttr.setWritable(False)
    nAttr.setStorable(False)

    Wheel.addAttribute(Wheel.aInput)
    
    Wheel.addAttribute(Wheel.bInput)

    Wheel.addAttribute(Wheel.aOutput)  

    Wheel.attributeAffects(Wheel.aInput, Wheel.aOutput)
    Wheel.attributeAffects(Wheel.bInput, Wheel.aOutput)



def initializePlugin(mobject):
    vendor = 'Sid'
    mplugin = omx.MFnPlugin(mobject,vendor)
    try:
        mplugin.registerNode(kPluginNodeTypeName,kPluginNodeId, nodeCreator,nodeInitializer)

    except:
        sys.stderr.write( "Failed to register node: %s" % kPluginNodeTypeName )

        raise

def uninitializePlugin(mobject):
    mplugin = omx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)

    except:
        sys.stderr.write( "Failed to De-register node: %s" % kPluginNodeTypeName )

        raise

