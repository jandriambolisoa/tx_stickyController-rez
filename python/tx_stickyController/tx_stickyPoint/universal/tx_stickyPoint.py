import math
import sys
import maya.OpenMaya as om
import maya.OpenMayaMPx as omp

kPluginNodeTypeName = 'stickyPoint'
kPluginNodeId = om.MTypeId(0x0012ba40)


class StickyPoint(omp.MPxNode):
    inputMesh = om.MObject()
    vertexId = om.MObject()
    outputTranslate = om.MObject()

    def __init__(self):
        omp.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        dhVertex = dataBlock.outputValue(StickyPoint.vertexId)
        inputVertexInt = dhVertex.asInt()

        dhMesh = dataBlock.inputValue(StickyPoint.inputMesh)
        inputMesh = dhMesh.asMesh()
        m = om.MFnMesh(inputMesh)
        vtx = om.MPoint()
        m.getPoint(inputVertexInt, vtx, om.MSpace.kWorld)

        outputHandle = dataBlock.outputValue(StickyPoint.outputTranslate)
        outputHandle.set3Double(vtx.x, vtx.y, vtx.z)

        dataBlock.setClean(plug)


def nodeCreator():
    return omp.asMPxPtr(StickyPoint())


def nodeInitializer():
    # input Mesh
    inputMeshAttr = om.MFnTypedAttribute()
    StickyPoint.inputMesh = inputMeshAttr.create('inputMesh', 'im', om.MFnMeshData.kMesh)

    # vertex ids
    vertexIdAttr = om.MFnNumericAttribute()
    StickyPoint.vertexId = vertexIdAttr.create('vertexId', 'vid', om.MFnNumericData.kInt)

    # output Translate
    outputTranslateAttr = om.MFnNumericAttribute()
    StickyPoint.outputTranslate = outputTranslateAttr.create('outputTranslate', 'out', om.MFnNumericData.k3Double)

    # add attributtes
    StickyPoint.addAttribute(StickyPoint.inputMesh)
    StickyPoint.addAttribute(StickyPoint.vertexId)
    StickyPoint.addAttribute(StickyPoint.outputTranslate)
    StickyPoint.attributeAffects(StickyPoint.inputMesh, StickyPoint.outputTranslate)
    StickyPoint.attributeAffects(StickyPoint.vertexId, StickyPoint.outputTranslate)


def initializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject, 'Txispy', '1.0', 'Any')
    try:
        mplugin.registerNode(kPluginNodeTypeName, kPluginNodeId, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write('Failed to register node: %s' % kPluginNodeTypeName)
        raise


def uninitializePlugin(mobject):
    mplugin = omp.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        sys.stderr.write('Failed to deregister node: %s' % kPluginNodeTypeName)
        raise
