'''
The script should work with any rig with a clean deform joints hierarchy
Work with referenced models and referenced rigs, just make sure to remove the skin cluster of the original models
Save a backup file and save often when using the script

Input the top Joints, middle or right side only, if lelf side joints are there: skip
'''

import maya.cmds as cmds
import maya.mel as mel
import itertools
import ast

# Left side axis, look like Maya keep this left side axis
leftSideAxis = "+x"

# MODELS: Models to skin
models = []
modelsTF = "models_text_field"
tempModel = None

# Root Joint (only one), need condition to check (len(rootJnts)>1)
rootJnts = []
rootJntsTF = "root_joints_text_field"
torsoJointsLists = []

# all joints list (flat list), for visibility
allJointsList = []

# Top Arm & Wing Joint(s)
topArmJnts = []
topArmJntsTF = "top_arm_joints_text_field"
armJointsLists = []

# Top Leg Joint(s)
topLegJnts = []
topLegJntsTF = "top_leg_joints_text_field"
legJointsLists = []

# Top Tail(s) & Tentacle Joint(s)
topTailJnts = []
topTailJntsTF = "top_tail_joints_text_field"
tailJointsLists = []

# Top Neck Joint(s), will include the head joint(s) & facial joints, but it will filter out facial joints if skip facial joints is checked
topNeckJnts = []
topNeckJntsTF = "top_neck_joints_text_field"
neckJointsLists = []

# Head Joint(s): optional, for facial joints, and to skip facial joints if needed
headJnts = []
headJntsTF = "head_joints_text_field"
facialJointsLists = []

# Skip facial joints check box, if checked, remove these facial joints from Head joints list (the list is no more needed) & Neck joints list
skipFacialJoints = False
skipFacialJointsTF = "skip_facial_joints_text_field"

deformJointsListFTW = []

currentJoint = None

trsUI_ID = "Faces_To_Weight"
jointSizeFloatSlider = "joint_size_slider"

# how to store the variables
# query existing variables (from models >> skip facial joints) 
# and run it every time open the script
def createInfoLoc():
    if not cmds.objExists("infoLoc_FTW"):
        infoLoc = cmds.spaceLocator(name="infoLoc_FTW")[0]
        cmds.addAttr(infoLoc, longName='models', dt='string')
        cmds.addAttr(infoLoc, longName='rootJnts', dt='string')
        cmds.addAttr(infoLoc, longName='topArmJnts', dt='string')
        cmds.addAttr(infoLoc, longName='topLegJnts', dt='string')
        cmds.addAttr(infoLoc, longName='topTailJnts', dt='string')
        cmds.addAttr(infoLoc, longName='topNeckJnts', dt='string')
        cmds.addAttr(infoLoc, longName='headJnts', dt='string')
        cmds.addAttr(infoLoc, longName='skipFacialJoints', dt='string')
        # set scale
        cmds.setAttr(infoLoc+"Shape.localScaleX", 0.012)
        cmds.setAttr(infoLoc+"Shape.localScaleY", 0.012)
        cmds.setAttr(infoLoc+"Shape.localScaleZ", 0.012)

        cmds.select(clear=1)

# convert string into list to store back the variables
def convertStrListIntoList(stringList):
    if stringList:
        stringList = ast.literal_eval(stringList)
        return stringList
    else:
        return []

# convert string to boolean
def str2bool(v):
    if v:
        return str(v).lower() in ("yes", "true", "t", "1")
    return False

# check existing variables in the locator when the script starts
def checkExistingVariables():
    global models
    global rootJnts
    global topArmJnts
    global topLegJnts
    global topTailJnts
    global topNeckJnts
    global headJnts
    global skipFacialJoints
    if cmds.objExists("infoLoc_FTW"):
        models = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.models"))
        rootJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.rootJnts"))
        topArmJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.topArmJnts"))
        topLegJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.topLegJnts"))
        topTailJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.topTailJnts"))
        topNeckJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.topNeckJnts"))
        headJnts = convertStrListIntoList(cmds.getAttr("infoLoc_FTW.headJnts"))
        skipFacialJoints = str2bool(cmds.getAttr("infoLoc_FTW.skipFacialJoints"))
    if not models and not rootJnts and not topArmJnts and not topLegJnts and not topTailJnts and not topNeckJnts and not headJnts and cmds.objExists("infoLoc_FTW"):
        cmds.delete("infoLoc_FTW")

checkExistingVariables()

# model check, check if the channels are locked or skin cluster exists
# check namespace of the model. Will namespace is important?
def modelCheck(modelsList):
    for model in modelsList:
        if mel.eval('findRelatedSkinCluster ' + model):
            raise Exception(model+" already has a skincluster")

# find current namespace
def checkNamespace(itemsList):
    if ":" in itemsList[-1]:
        nameSpace = itemsList[-1].rpartition(':')[0]+":"
        return nameSpace
    else:
        return ""

def prepTheTempModel(models):
    global tempModel
    # this function will duplicate the original models
    # combine them together and combine with a cube
    # show this model with the current joint to submit
    if models:    
        tempCube = cmds.polyCube(depth=0.01, height=0.01, width=0.01, ch=0)
        dupModels = cmds.duplicate(models)
        tempModel = cmds.polyUnite(dupModels, tempCube, name="tempModel_FTW", ch=0)[0]
        return tempModel
    else:
        raise Exception("models variable is missing")

def checkRootJointList(rootJnts):
    # need to be only 1 root joint
    if len(rootJnts) > 1:
        raise Exception("Please input 1 root joint only")

# filter out objects are not joints
def removeNotJoints(jntList):
    pureJointsList = []
    for jnt in jntList:
        if cmds.objectType(jnt)=="joint":
            pureJointsList.append(jnt)
    return pureJointsList

# filter out last joints
def filterLastJoints(jntList):
    noEndJointsList = []
    for jnt in jntList:
        if cmds.listRelatives(jnt, children=1):
            noEndJointsList.append(jnt)
    return noEndJointsList

# filter out joints in other lists, use for Neck Joints & Torso Joints
def filterOutMatchingJoints(jointLists, otherJointLists):
    clearJointLists=[]
    for jointList in jointLists:
        clearJointList = []
        for jnt in jointList:
            for otherJointList in otherJointLists:
                if jnt not in otherJointList:
                    clearJointList.append(jnt)
        if clearJointList:
            clearJointLists.append(clearJointList)
    return clearJointLists

# Filter out left side top joints
def filterOutLeftSide(jointList):
    rightSideJointList = []
    if leftSideAxis == "+x":
        num = 0
    
    for jnt in jointList:
        axisValue = cmds.xform(jnt,q=1,ws=1, rp=1)[num]
        if axisValue < 0.0001:
            rightSideJointList.append(jnt)
    return rightSideJointList

# List children joints using top joints
def listChildrenJoints(topJointName):
    jointsList = cmds.listRelatives(topJointName, children=1, allDescendents=1)
    # need to add Root joint as well
    jointsList.append(topJointName)
    return jointsList

# Sort joints in jointsList by number of parents & number of childrens
def sortCondition(jnt):
    parentPath = cmds.listRelatives(jnt, parent=1, fullPath=1)[0]
    parentNum = parentPath.count('|')
    # when joints have the same hierarchy, compare number of children
    childrenNum = -len(cmds.listRelatives(jnt, children=1))
    return parentNum, childrenNum

def sortJointListUsingSortCondition(jntList):
    jntList.sort(key = sortCondition)
    jntList.reverse()
    return jntList

# create joint lists
def createJointLists(topJointsList):
    jointLists = []
    if topJointsList:
        for topJnt in topJointsList:
            if cmds.objExists(topJnt) and cmds.objectType(topJnt)=="joint":
                jointList = listChildrenJoints(topJnt)
                jointList = removeNotJoints(jointList)
                jointList = filterLastJoints(jointList)
                jointList = filterOutLeftSide(jointList)
                jointList = sortJointListUsingSortCondition(jointList)
                jointLists.append(jointList)
            else:
                print(topJnt+" doesn't exist or not a joint")
    # return list(s) inside a list
    return jointLists

# create all joint list
def createAllJointList(rootJntsList):
    rootJnt = rootJntsList[0]
    if rootJnt:
        allJointsList = listChildrenJoints(rootJnt)
        allJointsList = removeNotJoints(allJointsList)
    else:
        raise Exception("There is no root joint")
    return allJointsList

# flat out list to do joint by joint for deformJointsListFTW
def flatoutList(flatList, inputListsofList):
    for inputList in inputListsofList:
        for item in inputList:
            flatList.append(item)
    return flatList

def createDeformJointsListFTW():
    global deformJointsListFTW
    global allJointsList
    
    # all joint list
    if not rootJnts:
        raise Exception("Root Joint is missing")
    else:
        allJointsList = createAllJointList(rootJnts)

    # Arm joint lists
    if topArmJnts:
        armJointsLists = createJointLists(topArmJnts)
        print(str(armJointsLists)+" are arm joint lists")

    # Leg joint lists
    if topLegJnts:
        legJointsLists = createJointLists(topLegJnts)
        print(str(legJointsLists)+" are leg joint lists")

    # Tail joint lists
    if topTailJnts:
        tailJointsLists = createJointLists(topTailJnts)
        print(str(tailJointsLists)+" are tail joint lists")

    # Facial joint lists
    if headJnts:
        facialJointsLists = createJointLists(headJnts)
        print(str(facialJointsLists)+" are facial joint lists")

    # Neck joint lists
    if topNeckJnts:
        if facialJointsLists:
            neckJointsLists = createJointLists(topNeckJnts)
            neckJointsLists = filterOutMatchingJoints(neckJointsLists, facialJointsLists)
            # insert head joint into the list if facial joints are skipped
            #for headJoint in headJnts:
            #    headJointParent = cmds.listRelatives(headJoint, parent=1)[0]
            #    for neckJointsList in neckJointsLists:
            #        if headJointParent in neckJointsList:
            #            neckJointsList.insert(0, headJoint)
        else:
            neckJointsLists = createJointLists(topNeckJnts)
        print(str(neckJointsLists)+" are neck joint lists")

    # Torso joint lists: list inside a list as well, for consistency
    if rootJnts:
        torsoJointsLists = createJointLists(rootJnts)
        if topArmJnts:
            torsoJointsLists = filterOutMatchingJoints(torsoJointsLists, armJointsLists)
        if topLegJnts:
            torsoJointsLists = filterOutMatchingJoints(torsoJointsLists, legJointsLists)
        if topTailJnts:
            torsoJointsLists = filterOutMatchingJoints(torsoJointsLists, tailJointsLists)
        if headJnts:
            if facialJointsLists:
                torsoJointsLists = filterOutMatchingJoints(torsoJointsLists, facialJointsLists)
        if topNeckJnts:
            torsoJointsLists = filterOutMatchingJoints(torsoJointsLists, neckJointsLists)
        print(str(torsoJointsLists)+" are torso joint lists")

    if topArmJnts:
        deformJointsListFTW = flatoutList(deformJointsListFTW, armJointsLists)
    if topLegJnts:
        deformJointsListFTW = flatoutList(deformJointsListFTW, legJointsLists)
    if topTailJnts:
        deformJointsListFTW = flatoutList(deformJointsListFTW, tailJointsLists)
    if headJnts:
        if facialJointsLists and not skipFacialJoints:
            deformJointsListFTW = flatoutList(deformJointsListFTW, facialJointsLists)
    if topNeckJnts:
        deformJointsListFTW = flatoutList(deformJointsListFTW, neckJointsLists)

    deformJointsListFTW = flatoutList(deformJointsListFTW, torsoJointsLists)
    print(str(deformJointsListFTW)+" are flatten joint list")
    if not deformJointsListFTW:
        raise Exception("Cannot create the deformJointsListFTW")

    return deformJointsListFTW

# checking current face components if it's valid or not
def checkingCurrentFaceComponents(selFaceComponents):
    # if nothing selected, return False >> if user select nothing and hit submit anyway >> create nothing and move to next joint
    # if not face component, raise Error
    for item in selFaceComponents:
        if '.f[' not in item:
            raise Exception("please select face components only")
    return True

# use selection set (instead of extracting models) for face components. Need to figure out how to food skin weight to these face later?
def submitFaceComponents(selFaceComponents, currentJoint):
    if checkingCurrentFaceComponents(selFaceComponents):
        # create selection Set from current face selection
        setName=currentJoint+"_FTWSet"
        if cmds.objExists(setName):
            cmds.sets(selFaceComponents, addElement=setName)
        else:
            cmds.sets(selFaceComponents, name=setName)

        try:
            cmds.hide(selFaceComponents)
        except:                    
            modelName = selFaceComponents[0].rpartition(".")[0]
            cmds.hide(modelName)
        # submit then hide
        cmds.setAttr(currentJoint + ".drawStyle", 2)
        cmds.select(clear=1)

def findPreviousJoint(currentJoint, jointList):
    index = jointList.index(currentJoint)
    if index-1 >= 0:
        previousJoint = str(jointList[index-1])
        return previousJoint
    return None

# find the next joint in FTW joint list
def findNextJoint(currentJoint, jointList):
    index = jointList.index(currentJoint)
    print(index)
    if index+1 < len(jointList):
        nextJoint = str(jointList[index+1])
        print(nextJoint)
        return nextJoint
    elif index+1 == len(jointList):
        showAllJoints()
        showAllFTWSetsMembers()
        cmds.showHidden(models)
        return currentJoint
    else:
        return None

# check current joint based on visibility of joints
def findCurrentFTWJointBasedOnJointVisibility():
    global allJointsList
    global rootJnts
    global currentJoint
    if cmds.getAttr(rootJnts[0]+".drawStyle") == 2:
        for joint in allJointsList:
            if cmds.getAttr(joint+".drawStyle") == 0:
                currentJoint = joint
                return currentJoint
    return False

def defaultCurrentJoint(jointList):
    global currentJoint
    # if no FTWSets, no selected joint, the default joint is the first one in the joint list
    currentJoint = jointList[0]
    return currentJoint

def findCurrentFTWJointBasedOnFTWSets(jointList):
    global currentJoint
    currentJoint = None
    # if no selected joint, the process starts based on the FTWSets
    setsList = cmds.ls(type="objectSet")

    # if FTWSets exist, the current joint is the joint with max index in FTWJointList
    maxIndex = 0
    for set in setsList:
        if set.endswith("_FTWSet"):
            # if existing FTW sets, then hide all the face that already have FTW_sets when hit Prep
            # if the face cannot be hidden, then hide the geometry
            setsFaceComponents = cmds.sets(set, q=True)
            try:
                cmds.hide(setsFaceComponents)
            except:
                modelName = setsFaceComponents[0].rpartition(".")[0]
                cmds.hide(modelName)
            jointName = set.replace('_FTWSet', '')
            if not cmds.objExists(jointName):
                raise Exception(jointName+" doesn't exist")
            # if the joint is not in the deformJointsListFTW, raise error
            if jointName not in jointList: 
                raise Exception("this joint is not from the deform joints of the character")
            jointNameIndex = jointList.index(jointName)
            if jointNameIndex >= maxIndex:
                maxIndex = jointNameIndex
                currentJoint = jointName
                # if the FTWSet is already there, it means this joint is already done face selection
                currentJoint = findNextJoint(currentJoint, jointList)
    return currentJoint

# find current joint based on joint selection
def findCurrentFTWJointBasedOnSelection(jointList, selectedItems):
    global currentJoint
    currentJoint = None
    # if a joint is selected before hitting "Prep"
    # if there is a selected joint >> the selected joint is the current joint
    if len(selectedItems) > 1 :
        return False

    if cmds.objectType(selectedItems[0]) !="joint":
        return False       

    currentJoint = selectedItems[0]

    # if the selected joint is the end joint, move up 1 level, check if it's ftw joints, then start from this joint
    if not cmds.listRelatives(currentJoint, children=1):
        currentJoint = cmds.listRelatives(currentJoint, parent=1)[0]

    # if the joint is not in the deformJointsListFTW, raise error
    if currentJoint not in jointList: 
        return False
    return currentJoint

# check how many time current joint appear in the list, if > 1, then raise Error
def checkValidCurrentJoint(currentJoint, jointList):
    if jointList.count(currentJoint) > 1:
        raise Exception("there are 2 same joints in the deform joint list")

# find the current joint to isolate it in the viewport
def findCurrentFTWJoint(jointList):
    global currentJoint
    currentJoint = None

    # first check current joint base on the visibility of joint, this one is to fix current joint when using UNDO
    if findCurrentFTWJointBasedOnJointVisibility():
        currentJoint = findCurrentFTWJointBasedOnJointVisibility()
        checkValidCurrentJoint(currentJoint, jointList)
        return currentJoint

    # if there is a selection, check if it's deform joint, and start from there, else, find FTWSets for current joint and lastly default value
    if cmds.ls(sl=1):
        if findCurrentFTWJointBasedOnSelection(jointList, cmds.ls(sl=1)):
            currentJoint = findCurrentFTWJointBasedOnSelection(jointList, cmds.ls(sl=1))        
        else:
            if findCurrentFTWJointBasedOnFTWSets(jointList):
                currentJoint = findCurrentFTWJointBasedOnFTWSets(jointList)
            else:
                currentJoint = defaultCurrentJoint(jointList)
        checkValidCurrentJoint(currentJoint, jointList)
        return currentJoint

    if findCurrentFTWJointBasedOnFTWSets(jointList):
        currentJoint = findCurrentFTWJointBasedOnFTWSets(jointList)
    else:
        currentJoint = defaultCurrentJoint(jointList)  
    checkValidCurrentJoint(currentJoint, jointList)         
    return currentJoint

# hide all joints
def hideAllJoints():
    global allJointsList
    for joint in allJointsList:
        # draw style = 2 is hidden
        cmds.setAttr(joint + ".drawStyle", 2)

# show all joints
def showAllJoints():
    global allJointsList
    for joint in allJointsList:
        # draw style = 0 is visible
        cmds.setAttr(joint + ".drawStyle", 0)

def isolateItems(jointsList, modelsList):
    # isolate Jiggle Joints Grp and Blendshape Mesh
    # make sure to click/ be active at viewport window (perspective camera)
    # query current camera
    if not modelsList:
        raise Exception("Model list is missing")

    currentSelection = cmds.ls(sl=1)
    panelList = cmds.getPanel(type='modelPanel')
    panel = cmds.getPanel(wf=True)
    print(panel)

    if panel not in panelList:
        raise Exception("The current panel is not viewport, please active the mouse at viewport")

    # select Jiggle Joints Grp and Blendshape Mesh
    cmds.select(modelsList, jointsList, replace=1)
    isoCrnt = cmds.isolateSelect(panel, q=True, s=True)
    mel.eval('enableIsolateSelect %s %d' % (panel, not isoCrnt))
    cmds.select(clear=1)

    if currentSelection:
        cmds.select(currentSelection, replace=1)

    # xray joints
    for panel in panelList:
        cmds.modelEditor(panel, e=1, jointXray=1)

def disableIsolateItems():
    panelList = cmds.getPanel(type='modelPanel')
    panel = cmds.getPanel(wf=True)
    print(panel)
    if panel not in panelList:
        raise Exception("The current panel is not viewport")
    cmds.isolateSelect(panel, state=0)
    cmds.select(clear=1)

def showAdvancedSkeletonJoints():
    global deformJointsListFTW
    # check rig namespace turn on joint visibility of advanced skeleton
    rigNamespace = checkNamespace(deformJointsListFTW)
    try:
        cmds.setAttr(rigNamespace+":Main.jointVis", 1)
    except:
        pass

def prep():
    global deformJointsListFTW
    deformJointsListFTW = []
    global currentJoint
    currentJoint = None
    global allJointsList
    global models
    global tempModel

    # create tempModel
    if models and not cmds.objExists("tempModel_FTW"):
        tempModel = prepTheTempModel(models)
    else:
        tempModel = "tempModel_FTW"

    # create ftw deform joints list
    createDeformJointsListFTW()
    # show all joints for the case of switching current joint mid way
    showAllJoints()
    # find current joint & show the current joint
    currentJoint = findCurrentFTWJoint(deformJointsListFTW)
    # hide all the joint (from root down)
    hideAllJoints()

    cmds.setAttr(currentJoint + ".drawStyle", 0)
    # isolate the models (in the list) and the current joint on the viewport
    isolateItems(allJointsList, tempModel)

    showAdvancedSkeletonJoints()

    # disable joint selection
    cmds.selectType(joint=0)

def showAllFTWSetsMembers():
    setsList = cmds.ls(type="objectSet")
    for set in setsList:
        if set.endswith("_FTWSet"):
            setsFaceComponents = cmds.sets(set, q=True)
            if setsFaceComponents:
                cmds.showHidden(setsFaceComponents)
                modelName = setsFaceComponents[0].rpartition(".")[0]
                cmds.showHidden(modelName)

# user can assign this function to a hotkey
def submit():
    global deformJointsListFTW
    global currentJoint
    global models
    # re-define current joint, due to Undo might broke the code, STILL BROKEN HERE
    currentJoint = findCurrentFTWJoint(deformJointsListFTW)

    selectedFaces = cmds.ls(sl=1)
    submitFaceComponents(selectedFaces, currentJoint)
    # find the next joint, then show the next joint
    currentJoint = findNextJoint(currentJoint, deformJointsListFTW)
    if currentJoint:
        cmds.setAttr(currentJoint + ".drawStyle", 0)
    else:
        # if no next joint, show all the joint again (from root joint down)
        showAllJoints()
        # show all the face component and the models
        showAllFTWSetsMembers()
        # show all the models
        cmds.showHidden(models)

def previous():
    global deformJointsListFTW
    global currentJoint
    currentJoint = findCurrentFTWJoint(deformJointsListFTW)
    cmds.setAttr(currentJoint + ".drawStyle", 2)
    currentJoint = findPreviousJoint(currentJoint, deformJointsListFTW)
    cmds.setAttr(currentJoint + ".drawStyle", 0)
    # show again the hidden face component, if FTWSet exists
    if cmds.objExists(currentJoint+"_FTWSet"):
        facesList = cmds.sets(currentJoint+"_FTWSet", q=True )
        cmds.showHidden(facesList)
        # clear the face component from FTWSet, and user need to submit again
        cmds.sets(facesList, remove=currentJoint+"_FTWSet")

def facesToVertices(faceList):
    verticesList = cmds.polyListComponentConversion(faceList, ff=True, tv =True)
    return verticesList

def floodSkinByJointName(currentSkinCluster, verticesList, jointName):
    cmds.skinPercent(currentSkinCluster, verticesList, transformValue=[(jointName, 1)])

def bindSkinFTW():
    global deformJointsListFTW
    global models
    global tempModel
    global allJointsList

    if not tempModel:
        if cmds.objExists("tempModel_FTW"):
            tempModel = "tempModel_FTW"
        else:
            raise Exception("tempModel_FTW doesn't exist")

    # delete the skin cluster in case it's existing
    cmds.delete(tempModel, constructionHistory = True)

    if not deformJointsListFTW:
        prep()

    # show all before binding
    showAllJoints()
    showAllFTWSetsMembers()
    cmds.showHidden(models)

    # filter out end joints
    allJointsListNoEnd = filterLastJoints(allJointsList)

    # query the face components in _FTWSets, if having items, then flood the face component to the specific joints
    # mirror the skin weight from right to left

    tempModelSkinCluster = cmds.skinCluster(allJointsListNoEnd, tempModel, sm=0, tsb=True)[0]
    for jointName in deformJointsListFTW:
        if cmds.objExists(jointName+"_FTWSet"):
            facesList = cmds.sets(jointName+"_FTWSet", q=True)
            if facesList:
                verticesList = facesToVertices(facesList)
                if verticesList:
                    floodSkinByJointName(tempModelSkinCluster, verticesList, jointName)

    # mirror the skin weight from right to left
    cmds.copySkinWeights(ss=tempModelSkinCluster, ds=tempModelSkinCluster, mm="YZ", mi=1, sa="closestPoint", ia="closestJoint")

    # delete existing skin cluster if users are not using referenced models
    if not checkNamespace(models):
        for model in models:
            cmds.delete(model, constructionHistory = True)
    
    # copy the skin weight over the original models
    for model in models:
        modelSkinCluster = cmds.skinCluster(allJointsListNoEnd, model, sm=0, tsb=True)[0]       
        cmds.copySkinWeights(ss=tempModelSkinCluster, ds=modelSkinCluster, nm=True, surfaceAssociation='closestPoint')
    
    cmds.hide(tempModel)
    disableIsolateItems()

# Use ngskin to smooth all the weight (user will do it themselves)
def smoothSkinFTW():
    # if there are selected vertexes, smooth selected vertexes only
    pass

def cleanUp():
    # delete all FTW selection sets
    setsList = cmds.ls(type="objectSet")

    # if FTWSets exist, the current joint is the joint with max index in FTWJointList
    for set in setsList:
        if set.endswith("_FTWSet"):
            cmds.delete(set)

    # delete the temp model
    if cmds.objExists("tempModel_FTW"):
        cmds.delete("tempModel_FTW")
    
    if cmds.objExists("infoLoc_FTW"):
        cmds.delete("infoLoc_FTW")

# need a slider to adjust joint size here, joint need to be selectable, in case user need to know the joint name

# The below need a collapsing arrow

def toggleJointSelection():
    currentJointSelectionStatus = cmds.selectType(q=1, joint=1)
    if currentJointSelectionStatus:
        cmds.selectType(joint=0)
    else:
        cmds.selectType(joint=1)

def manualAdjustJointSize():
    global jointSizeFloatSlider
    jointSize = cmds.floatSlider(jointSizeFloatSlider, q=True, v=True)
    cmds.jointDisplayScale(jointSize, a=1)

def load_selected_as(sel, text_field):
    text_field = cmds.textField(text_field, e=True, tx=str(sel))

def chooseModels():
    global models
    models = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()

    load_selected_as(models, modelsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.models", models, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

    modelCheck(models)

def chooseRootJoints():
    global rootJnts
    rootJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()

    load_selected_as(rootJnts, rootJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.rootJnts", rootJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def chooseTopArmJoints():
    global topArmJnts
    topArmJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()
    load_selected_as(topArmJnts, topArmJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.topArmJnts", topArmJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def chooseTopLegJoints():
    global topLegJnts
    topLegJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()
    load_selected_as(topLegJnts, topLegJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.topLegJnts", topLegJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def chooseTopTailJoints():
    global topTailJnts
    topTailJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()
    load_selected_as(topTailJnts, topTailJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.topTailJnts", topTailJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def chooseTopNeckJoints():
    global topNeckJnts
    topNeckJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()
    load_selected_as(topNeckJnts, topNeckJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.topNeckJnts", topNeckJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def chooseHeadJoints():
    global headJnts
    headJnts = cmds.ls(sl=1)
    # start creating info locator when there is input
    createInfoLoc()
    load_selected_as(headJnts, headJntsTF)
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.headJnts", headJnts, type="string")
    else:
        raise Exception("infoLoc_FTW is missing")

def checkBoxOn():
    global skipFacialJoints
    skipFacialJoints = True
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.skipFacialJoints", skipFacialJoints, type="string")


def checkBoxOff():
    global skipFacialJoints
    skipFacialJoints = False
    if cmds.objExists("infoLoc_FTW"):
        cmds.setAttr("infoLoc_FTW.skipFacialJoints", skipFacialJoints, type="string")

def show_UI(winID):
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)
    cmds.window(winID)
    create_UI(winID)
    cmds.showWindow(winID)

def create_UI(winID):
    global jointSizeFloatSlider
    global modelsTF
    global rootJntsTF
    global topArmJntsTF
    global topLegJntsTF
    global topTailJntsTF
    global topNeckJntsTF
    global headJntsTF
    global skipFacialJointsTF

    toolWindowWidth = 500
    # Make a new window
    window = cmds.window(winID, e=True, width=toolWindowWidth, height=540, title="FACES TO WEIGHT")

    # layout
    columnMain = cmds.columnLayout() 

    # Title
    mainLayout = cmds.rowLayout(numberOfColumns=1, p=columnMain)
    cmds.text(label='\n FACES TO WEIGHT \n', p=mainLayout, width=toolWindowWidth, font="boldLabelFont")
    cmds.text(label='gumroad.com/TruongCgArtist\n', p=columnMain, width=toolWindowWidth)

    selectionTypeRow = cmds.rowLayout(numberOfColumns=2, p=columnMain)
    cmds.iconTextButton(label="Toggle Joint Selection", p=selectionTypeRow, width=toolWindowWidth*1/6, i='kinJoint.png', command='toggleJointSelection()')
    jointSizeFloatSlider = cmds.floatSlider(min=0.01, max=10, value=2, step=0.01, width=toolWindowWidth*4/6, dc='manualAdjustJointSize()')

    cmds.separator(w=toolWindowWidth, h=10, p=columnMain)


    form = cmds.formLayout(p=columnMain)
    inputTab = cmds.frameLayout(p=form, collapsable=1, l="INPUT")

    # models
    loadModelsItemsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_modelsItems = cmds.textField(modelsTF, w=toolWindowWidth*0.7, h=20, p=loadModelsItemsRow, ed=0)
    if models:
        cmds.textField(tf_modelsItems, e=True, tx=str(models))
    cmds.button(label='Models', width=toolWindowWidth*0.3, align='right', p=loadModelsItemsRow, command='chooseModels()')

    # root joint
    loadRootJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_rootJntsItems = cmds.textField(rootJntsTF, w=toolWindowWidth*0.7, h=20, p=loadRootJntsRow, ed=0)
    if rootJnts:
        cmds.textField(tf_rootJntsItems, e=True, tx=str(rootJnts))
    cmds.button(label='Root Joint', width=toolWindowWidth*0.3, align='right', p=loadRootJntsRow, command='chooseRootJoints()')

    # top arm joints
    loadTopArmJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_topArmJntsItems = cmds.textField(topArmJntsTF, w=toolWindowWidth*0.7, h=20, p=loadTopArmJntsRow, ed=0)
    if topArmJnts:
        cmds.textField(tf_topArmJntsItems, e=True, tx=str(topArmJnts))
    cmds.button(label='Top Arm Joint(s)', width=toolWindowWidth*0.3, align='right', p=loadTopArmJntsRow, command='chooseTopArmJoints()')

    # top leg joints
    loadTopLegJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_topLegJntsItems = cmds.textField(topLegJntsTF, w=toolWindowWidth*0.7, h=20, p=loadTopLegJntsRow, ed=0)
    if topLegJnts:
        cmds.textField(tf_topLegJntsItems, e=True, tx=str(topLegJnts))
    cmds.button(label='Top Leg Joint(s)', width=toolWindowWidth*0.3, align='right', p=loadTopLegJntsRow, command='chooseTopLegJoints()')

    # top tail joints
    loadTopTailJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_topTailJntsItems = cmds.textField(topTailJntsTF, w=toolWindowWidth*0.7, h=20, p=loadTopTailJntsRow, ed=0)
    if topTailJnts:
        cmds.textField(tf_topTailJntsItems, e=True, tx=str(topTailJnts))
    cmds.button(label='Top Tail Joint(s)', width=toolWindowWidth*0.3, align='right', p=loadTopTailJntsRow, command='chooseTopTailJoints()')

    # top neck joints
    loadTopNeckJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_topNeckJntsItems = cmds.textField(topNeckJntsTF, w=toolWindowWidth*0.7, h=20, p=loadTopNeckJntsRow, ed=0)
    if topNeckJnts:
        cmds.textField(tf_topNeckJntsItems, e=True, tx=str(topNeckJnts))
    cmds.button(label='Top Neck Joint(s)', width=toolWindowWidth*0.3, align='right', p=loadTopNeckJntsRow, command='chooseTopNeckJoints()')

    # head joints
    loadHeadJntsRow = cmds.rowLayout(numberOfColumns=2, p=inputTab)
    tf_headJntsItems = cmds.textField(headJntsTF, w=toolWindowWidth*0.7, h=20, p=loadHeadJntsRow, ed=0)
    if headJnts:
        cmds.textField(tf_headJntsItems, e=True, tx=str(headJnts))
    cmds.button(label='Head Joint(s)', width=toolWindowWidth*0.3, align='right', p=loadHeadJntsRow, command='chooseHeadJoints()')

    # skip facial joints check box
    cmds.separator(w=toolWindowWidth, h=20, p=inputTab)
    loadHeadJntsRow = cmds.rowLayout(numberOfColumns=1, p=inputTab)
    ctrlBox1 = cmds.checkBox(label='Skip Facial Joints?', value=skipFacialJoints, onCommand='checkBoxOn()', offCommand='checkBoxOff()', p=loadHeadJntsRow)
    cmds.separator(w=toolWindowWidth, h=20, p=inputTab)

    form2 = cmds.formLayout(p=columnMain) 
    prepRow = cmds.rowLayout(numberOfColumns=1, p=form2)
    cmds.button(label="PREP", p=prepRow, width=toolWindowWidth, command='prep()')
    
    form3 = cmds.formLayout(p=columnMain)
    submitRow = cmds.rowLayout(numberOfColumns=2, p=form3)
    cmds.button(label="SUBMIT", p=submitRow, width=toolWindowWidth/2, command='submit()')
    cmds.button(label="<< PREVIOUS", p=submitRow, width=toolWindowWidth/2, command='previous()')
    

    form4 = cmds.formLayout(p=columnMain)
    bindSkinRow = cmds.rowLayout(numberOfColumns=2, p=form4)
    cmds.button(label="BIND", p=bindSkinRow, width=toolWindowWidth/2, command='bindSkinFTW()')
    # cmds.button(label="SMOOTH", p=bindSkinRow, width=toolWindowWidth/2, command='smoothSkinFTW()')

    form5 = cmds.formLayout(p=columnMain) 
    cleanUpRow = cmds.rowLayout(numberOfColumns=1, p=form5)
    cmds.button(label="CLEAN UP", p=cleanUpRow, width=toolWindowWidth, command='cleanUp()')

show_UI(trsUI_ID)

