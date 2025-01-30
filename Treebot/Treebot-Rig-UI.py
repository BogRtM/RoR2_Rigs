# context.area: VIEW_3D

#PLEASE READ THE README FOR A GUIDE ON HOW TO USE THIS RIG
#https://github.com/BogRtM/RoR2_Rigs
#Contact @bog_rtm on Discord for questions

import bpy

armatureName = "TreebotArmature"
rig_id = "TREEBOT_RIG_ID"

class TREEBOT_PT_RigUI(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "VIEW3D_PT_Treebot_RigUI"
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
class TREEBOT_PT_Visibility(bpy.types.Panel):
    bl_label = "Bone Visibility"
    bl_idname = "TREEBOT_PT_Visibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_RigUI.bl_idname
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
        row.prop(boneCollections["CTRL-Torso"], 'is_visible', toggle=True, text="TORSO")

        column.separator(factor = 1.5, type='LINE')
        
        #Flower
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Flower"], 'is_visible', toggle=True, text="FLOWER")
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Flower Tweak"], 'is_visible', toggle=True, text="FLOWER TWEAK")
        
        column.separator(factor = 1.5, type='LINE')
        
        #Arm
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Shoulder"], 'is_visible', toggle=True, text="SHOULDER")
        
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Weapon"], 'is_visible', toggle=True, text="FK-WEAPON", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Weapon"], 'is_visible', toggle=True, text="IK-WEAPON", icon = "CON_KINEMATIC")

        column.separator(factor = 1.5, type='LINE')
        
        #Legs
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Front Leg.L"], 'is_visible', toggle=True, text="FK-FRONT LEG.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Front Leg.R"], 'is_visible', toggle=True, text="FK-FRONT LEG.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Front Leg.L"], 'is_visible', toggle=True, text="IK-FRONT LEG.L", icon = "CON_KINEMATIC")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Front Leg.R"], 'is_visible', toggle=True, text="IK-FRONT LEG.R", icon = "CON_KINEMATIC")
        
        column.separator(factor = 1.5, type='LINE')
        
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Back Leg.L"], 'is_visible', toggle=True, text="FK-BACK LEG.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Back Leg.R"], 'is_visible', toggle=True, text="FK-BACK LEG.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Back Leg.L"], 'is_visible', toggle=True, text="IK-BACK LEG.L", icon = "CON_KINEMATIC")
        row=row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Back Leg.R"], 'is_visible', toggle=True, text="IK-BACK LEG.R", icon = "CON_KINEMATIC")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Leg Tweak"], 'is_visible', toggle=True, text="LEG TWEAK")

################################ Snapping ################################
class TREEBOT_OP_SNAP_MASTER(bpy.types.Operator):
    bl_idname = "treebot.snap_master"
    bl_label = ""
    bl_description = "Snap Arm IK/FK"
    bl_options = {'UNDO', 'INTERNAL'}

    #Collect the necessary info for the snap operation
    limb : bpy.props.StringProperty(name="'Front' or 'Back' or 'Weapon'")
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
    ctrlBoneDict = {}

    #Add the name of the CTRL bone you wish to snap to the list. Leave out the prefix and side of the bone as that will be added in the code below
    #MAKE SURE TO ADD THESE IN THE ORDER OF THE BONE HIERARCHY
    ctrlBoneDict[ctrlPrefix + 'Thigh.' + limb + '.' + side] = 'CTRL-IK-Thigh.' + limb + '.' + side
    ctrlBoneDict[ctrlPrefix + 'Calf.' + limb + '.' + side] = mchPrefix + 'Calf.' + limb + '.' + side
    ctrlBoneDict[ctrlPrefix + 'Foot.' + limb + '.' + side] = mchPrefix + 'Foot.' + limb + '.' + side

    #We iterate through the list of our CTRL bones and snap them to their associated MCH bone.
    for ctrlBoneName in ctrlBoneDict:
        ctrlBone = rigPose.bones.get(ctrlBoneName)
        if(rigPose.bones.get(ctrlBoneDict[ctrlBoneName])):
            ctrlBone = rigPose.bones.get(ctrlBoneName)
            mchBone = rigPose.bones.get(ctrlBoneDict[ctrlBoneName])
            #print(ctrlBone.name + " - " + mchBone.name)
            ctrlBone.matrix = mchBone.matrix.copy()
            bpy.context.view_layer.update()

    #Set limb to FK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb} Leg.{side} FK/IK'] = 0

#Snap IK to FK for selected limb then switch to IK
def IK_FK(limb:str, side:str):
    #The prefix for the CTRL and MCH bones. The CTRL-IK bones will be snapped to the MCH-SNAP-IK bones in this case.
    ctrlPrefix = 'CTRL-IK-'
    mchPrefix = 'MCH-SNAP-IK-'

    print("Snapping " + limb + "." + side + " IK to FK")

    rigPose = bpy.data.objects[armatureName].pose
    bpy.ops.pose.select_all(action='DESELECT')

    #Create an empty list which we will store our CTRL bones in
    ctrlBoneDict = {}

    #Add the name of the CTRL bone you wish to snap to the list. Leave out the prefix and side of the bone as that will be added in the code below
    #MAKE SURE TO ADD THESE IN THE ORDER OF THE BONE HIERARCHY
    ctrlBoneDict[ctrlPrefix + 'Foot.' + limb + '.' + side] = mchPrefix + 'Foot.' + limb + '.' + side

    #We iterate through the list of our CTRL bones and snap them to their associated MCH bone.
    for ctrlBoneName in ctrlBoneDict:
        ctrlBone = rigPose.bones.get(ctrlBoneName)
        if(rigPose.bones.get(ctrlBoneDict[ctrlBoneName])):
            ctrlBone = rigPose.bones.get(ctrlBoneName)
            mchBone = rigPose.bones.get(ctrlBoneDict[ctrlBoneName])
            #print(ctrlBone.name + " - " + mchBone.name)
            ctrlBone.matrix = mchBone.matrix.copy()
            bpy.context.view_layer.update()

    #Set limb to IK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb} Leg.{side} FK/IK'] = 1

class TREEBOT_PT_Snap_Utilities(bpy.types.Panel):
    bl_label = "Snap Utilities"
    bl_idname = "TREEBOT_PT_Snap Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        #Arms
        row = column.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="FRONT LEG.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Front'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="FRONT LEG.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Front'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="FRONT LEG.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Front'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="FRONT LEG.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Front'
        op.side = 'R'
        op.snapTo = 'IK-FK'

        column.separator(factor=1.5, type = 'LINE')

        #Legs
        row = column.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="BACK LEG.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Back'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="BACK LEG.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Back'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="BACK LEG.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Back'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("treebot.snap_master", emboss=True, text="BACK LEG.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Back'
        op.side = 'R'
        op.snapTo = 'IK-FK'

################################ Properties ################################ 
class TREEBOT_PT_Properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_idname = "TREEBOT_PT_Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class TREEBOT_PT_BodyProperties(bpy.types.Panel):
    bl_label = "Body Properties"
    bl_idname = "TREEBOT_PT_BodyProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['TreebotArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Upper Body Follow")
        row.split(align= True)
        row.prop(bone, '["Upper Body Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Upper Body Target")
        row.split(align= True)
        row.prop(bone, '["Upper Body Target"]', text = "", slider=True)

class TREEBOT_PT_WeaponProperties(bpy.types.Panel):
    bl_label = "Weapon Properties"
    bl_idname = "TREEBOT_PT_WeaponProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()
        
        bone = bpy.data.objects[armatureName].pose.bones['PROPERTIES']
        
        row = column.row(align=True)
        row.label(text = "Weapon FK/IK")
        row.split(align= True)
        row.prop(bone, '["Weapon FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Weapon Follow")
        row.split(align= True)
        row.prop(bone, '["Weapon Follow"]', text = "", slider=True)

class TREEBOT_PT_LegProperties(bpy.types.Panel):
    bl_label = "Leg Properties"
    bl_idname = "TREEBOT_PT_LegProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = TREEBOT_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects[armatureName].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Front Leg.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Front Leg.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Front Leg.R FK/IK")
        row.split(align= True)
        row.prop(bone, '["Front Leg.R FK/IK"]', text = "", slider=True)

        box = layout.box()
        column = box.column()

        row = column.row(align=True)
        row.label(text = "Back Leg.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Back Leg.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Back Leg.R FK/IK")
        row.split(align= True)
        row.prop(bone, '["Back Leg.R FK/IK"]', text = "", slider=True)

panels = (TREEBOT_PT_RigUI,
          TREEBOT_PT_Visibility, 
          TREEBOT_PT_Snap_Utilities, 
          TREEBOT_PT_Properties,
          TREEBOT_PT_BodyProperties,
          TREEBOT_PT_WeaponProperties,
          TREEBOT_PT_LegProperties,
          TREEBOT_OP_SNAP_MASTER
          )

register, unregister = bpy.utils.register_classes_factory(panels)

#Change __name__ == "__main__" if running from inside the Blender text editor
if __name__ == "<run_path>":
   register()