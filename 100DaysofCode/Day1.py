#Create Bendy Setup betwn 2 selected objects 
# select 2 positions
# Finding position for 2 points
sel = pm.ls(sl=1)
pos1 = sel[0]
pos2 = sel[1]


try:
    pm.select(pos1)
    tempPos = pm.cluster(n='Temp')[1]
    JntPos1 = pm.createNode('joint',n = (pos1+'_Pos1Jnt'))
    pm.delete(pm.parentConstraint(tempPos,JntPos1))
    pm.delete(tempPos)
    
    
    
    
except:
    tempPos = pm.createNode('transform',n = 'Temp')
    pm.delete(pm.parentConstraint(pos1,tempPos))
    JntPos1 = pm.createNode('joint',n = (pos1+'_Pos1Jnt'))
    pm.delete(pm.parentConstraint(tempPos,JntPos1))
    pm.delete(tempPos)

    

try:
    pm.select(pos2)
    tempPos = pm.cluster(n='Temp')[1]
    JntPos2 = pm.createNode('joint',n = (pos2+'_Pos2Jnt'))
    pm.delete(pm.parentConstraint(tempPos,JntPos2))
    pm.delete(tempPos)
    
    
    
    
except:
    tempPos = pm.createNode('transform',n = 'Temp')
    pm.delete(pm.parentConstraint(pos2,tempPos))
    JntPos2 = pm.createNode('joint',n = (pos2+'_Pos2Jnt'))
    pm.delete(pm.parentConstraint(tempPos,JntPos2))
    pm.delete(tempPos)
    



pm.parent(JntPos2,JntPos1)

pm.joint(JntPos1,e=1,oj = 'xyz',secondaryAxisOrient = 'yup')


