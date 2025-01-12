# context.area: VIEW_3D

#PLEASE READ THE README FOR A GUIDE ON HOW TO USE THIS RIG
#https://github.com/BogRtM/RoR2_Rigs
#Contact @bog_rtm on Discord for questions

import bpy

armatureName = "CommandoArmature"
rig_id = "COMMANDO_RIG_ID"

class COMMANDO_PT_RigUI(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "VIEW3D_PT_Commando_RigUI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    
    @classmethod
    def poll(self, context):
        try:
            return (context.active_object.data.get("rig_id") == rig_id)
        except (AttributeError, KeyError, TypeError):
            return False

    def draw(self, context):
        layout = self.layout

################################ Visibility ################################ 
class COMMANDO_PT_Visibility(bpy.types.Panel):
    bl_label = "Bone Visibility"
    bl_idname = "COMMANDO_PT_Visibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        boneCollections = bpy.data.armatures[armatureName].collections_all

        testCol = bpy.data.armatures[armatureName].collections

        column = layout.column()

        #Essentials
        row = column.row(align=True)
        row.prop(boneCollections["PROPERTIES"], 'is_visible', toggle=True, text="PROPERTIES")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-Root"], 'is_visible', toggle=True, text="ROOT")

        column.separator(factor = 1.5, type='LINE')

        #Torso
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Head"], 'is_visible', toggle=True, text="HEAD")
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Torso"], 'is_visible', toggle=True, text="TORSO")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-Torso Tweak"], 'is_visible', toggle=True, text="TORSO TWEAK")

        column.separator(factor = 1.5, type='LINE')

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Arm.L"], 'is_visible', toggle=True, text="FK-ARM.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Arm.R"], 'is_visible', toggle=True, text="FK-ARM.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Arm.L"], 'is_visible', toggle=True, text="IK-ARM.L", icon = "CON_KINEMATIC")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Arm.R"], 'is_visible', toggle=True, text="IK-ARM.R", icon = "CON_KINEMATIC")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Fingers.L"], 'is_visible', toggle=True, text="FINGERS.L")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-Fingers.R"], 'is_visible', toggle=True, text="FINGERS.R")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Gun.L"], 'is_visible', toggle=True, text="GUN.L")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-Gun.R"], 'is_visible', toggle=True, text="GUN.R")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Arm Tweak"], 'is_visible', toggle=True, text="ARM TWEAK")

        column.separator(factor = 1.5, type='LINE')
        
        #Legs
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Leg.L"], 'is_visible', toggle=True, text="FK-LEG.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Leg.R"], 'is_visible', toggle=True, text="FK-LEG.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Leg.L"], 'is_visible', toggle=True, text="IK-LEG.L", icon = "CON_KINEMATIC")
        row=row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Leg.R"], 'is_visible', toggle=True, text="IK-LEG.R", icon = "CON_KINEMATIC")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Leg Tweak"], 'is_visible', toggle=True, text="LEG TWEAK")

################################ Snapping ################################
class COMMANDO_OP_SNAP_MASTER(bpy.types.Operator):
    bl_idname = "commando.snap_master"
    bl_label = ""
    bl_description = "Snap Arm IK/FK"
    bl_options = {'UNDO', 'INTERNAL'}

    #Collect the necessary info for the snap operation
    limb : bpy.props.StringProperty(name="'Arm' or 'Leg'")
    side : bpy.props.StringProperty(name="'L' or 'R'")
    snapTo : bpy.props.StringProperty(name="'FK-IK' or 'IK-FK'")

    def execute(self, context):
        limb = self.limb
        side = self.side
        snapTo = self.snapTo
        
        #Depending on the value of snapTo, perform either FK>IK or IK>FK snapping
        if(snapTo == "FK-IK"):
            FK_IK(limb, side)
        elif(snapTo == "IK-FK"):
            IK_FK(limb, side)

        return {"FINISHED"}

#Snap FK to IK for selected limb then switch to FK
def FK_IK(limb:str, side:str):
    #The prefix for the CTRL-FK and MCH-IK bones. The CTRL-FK bones will be snapped to the MCH-IK bones in this case.
    #Make sure this matches the naming structure of your bones
    ctrlPrefix = 'CTRL-FK-'
    mchPrefix = 'MCH-IK-'

    print("Snapping " + limb + "." + side + " FK to IK")

    rigPose = bpy.data.objects[armatureName].pose
    bpy.ops.pose.select_all(action='DESELECT')

    #Create an empty list which we will store our CTRL bones in
    ctrlBoneList = []

    #Add the name of the CTRL bone you wish to snap to the list. Leave out the prefix and side of the bone as that will be added in the code below
    #MAKE SURE TO ADD THESE IN THE ORDER OF THE BONE HIERARCHY
    if(limb == "Arm"):
        ctrlBoneList.append("upper_arm.")
        ctrlBoneList.append("lower_arm.")
        ctrlBoneList.append("hand.")
    elif(limb == "Leg"):
        ctrlBoneList.append("thigh.")
        ctrlBoneList.append("calf.")
        ctrlBoneList.append("foot.")
        ctrlBoneList.append("toe.")

    #We iterate through the list of our CTRL bones and snap them to their associated MCH bone.
    for ctrlBoneName in ctrlBoneList:
        ctrlBone = rigPose.bones.get(ctrlPrefix + ctrlBoneName + side)
        if(rigPose.bones.get(mchPrefix + ctrlBoneName + side)):
            mchBone = rigPose.bones.get(mchPrefix + ctrlBoneName + side)
            ctrlBone.matrix = mchBone.matrix.copy()
            bpy.context.view_layer.update()

    #Set limb to FK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb}.{side} FK/IK'] = 0

#Snap IK to FK for selected limb then switch to IK
def IK_FK(limb:str, side:str):
    #The prefix for the CTRL and MCH bones. The CTRL-IK bones will be snapped to the MCH-SNAP-IK bones in this case.
    ctrlPrefix = 'CTRL-IK-'
    mchPrefix = 'MCH-SNAP-IK-'

    print("Snapping " + limb + "." + side + " IK to FK")

    rigPose = bpy.data.objects[armatureName].pose
    bpy.ops.pose.select_all(action='DESELECT')

    #Create an empty list which we will store our CTRL bones in
    ctrlBoneList = []

    #Add the name of the CTRL bone you wish to snap to the list. Leave out the prefix and side of the bone as that will be added in the code below
    #MAKE SURE TO ADD THESE IN THE ORDER OF THE BONE HIERARCHY
    if(limb == "Arm"):
        ctrlBoneList.append("Hand.")
        ctrlBoneList.append("Elbow.")
    elif(limb == "Leg"):
        ctrlBoneList.append("FootMaster.")
        ctrlBoneList.append("Knee.")
        ctrlBoneList.append("toe.")

    #We iterate through the list of our CTRL bones and snap them to their associated MCH bone.
    for ctrlBoneName in ctrlBoneList:
        ctrlBone = rigPose.bones.get(ctrlPrefix + ctrlBoneName + side)
        if(rigPose.bones.get(mchPrefix + ctrlBoneName + side)):
            mchBone = rigPose.bones.get(mchPrefix + ctrlBoneName + side)
            ctrlBone.matrix = mchBone.matrix.copy()
            bpy.context.view_layer.update()

    #Set limb to IK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb}.{side} FK/IK'] = 1

class COMMANDO_PT_Snap_Utilities(bpy.types.Panel):
    bl_label = "Snap Utilities"
    bl_idname = "COMMANDO_PT_Snap Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        #Arms
        row = column.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="ARM.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="ARM.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="ARM.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="ARM.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'R'
        op.snapTo = 'IK-FK'

        column.separator(factor=1.5, type = 'LINE')

        #Legs
        row = column.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="LEG.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="LEG.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="LEG.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("commando.snap_master", emboss=True, text="LEG.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'R'
        op.snapTo = 'IK-FK'

################################ Properties ################################ 
class COMMANDO_PT_Properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_idname = "COMMANDO_PT_Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class COMMANDO_PT_HeadProperties(bpy.types.Panel):
    bl_label = "Head Properties"
    bl_idname = "COMMANDO_PT_HeadProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['CommandoArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Head Follow")
        row.split(align= True)
        row.prop(bone, '["Head Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Head Target")
        row.split(align= True)
        row.prop(bone, '["Head Target"]', text = "", slider=True)

class COMMANDO_PT_ArmProperties(bpy.types.Panel):
    bl_label = "Arm Properties"
    bl_idname = "COMMANDO_PT_ArmProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['CommandoArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Arm.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Arm.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Arm.L Follow")
        row.split(align= True)
        row.prop(bone, '["Arm.L Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Arm.L IK Stretch")
        row.split(align= True)
        row.prop(bone, '["Arm.L IK Stretch"]', text = "", slider=True)

        box = layout.box()
        column = box.column()

        row = column.row(align=True)
        row.label(text = "Arm.R FK/IK")
        row.split(align= True)
        row.prop(bone, '["Arm.R FK/IK"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Arm.R Follow")
        row.split(align= True)
        row.prop(bone, '["Arm.R Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Arm.R IK Stretch")
        row.split(align= True)
        row.prop(bone, '["Arm.R IK Stretch"]', text = "", slider=True)


class COMMANDO_PT_LegProperties(bpy.types.Panel):
    bl_label = "Leg Properties"
    bl_idname = "COMMANDO_PT_LegProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = COMMANDO_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects[armatureName].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Leg.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Leg.L FK/IK"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Leg.L Follow")
        row.split(align= True)
        row.prop(bone, '["Leg.L Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Leg.L IK Stretch")
        row.split(align= True)
        row.prop(bone, '["Leg.L IK Stretch"]', text = "", slider=True)

        box = layout.box()
        column = box.column()

        row = column.row(align=True)
        row.label(text = "Leg.R FK/IK")
        row.split(align= True)
        row.prop(bone, '["Leg.R FK/IK"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Leg.R Follow")
        row.split(align= True)
        row.prop(bone, '["Leg.R Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Leg.R IK Stretch")
        row.split(align= True)
        row.prop(bone, '["Leg.R IK Stretch"]', text = "", slider=True)

panels = (COMMANDO_PT_RigUI,
          COMMANDO_PT_Visibility, 
          COMMANDO_PT_Snap_Utilities, 
          COMMANDO_PT_Properties,
          COMMANDO_PT_HeadProperties,
          COMMANDO_PT_ArmProperties,
          COMMANDO_PT_LegProperties,
          COMMANDO_OP_SNAP_MASTER
          )

register, unregister = bpy.utils.register_classes_factory(panels)

#Change __name__ == "__main__" if running from inside the Blender text editor
if __name__ == "<run_path>":
   register()