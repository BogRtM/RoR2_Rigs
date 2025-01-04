# context.area: VIEW_3D

#PLEASE READ THE README FOR A GUIDE ON HOW TO USE THIS RIG
#https://github.com/BogRtM/RoR2_Rigs
#Contact @bog_rtm on Discord for questions

import bpy

rig_id = "CHEF_RIG_ID"

class CHEF_PT_RigUI(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "VIEW3D_PT_Chef_RigUI"
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
class CHEF_PT_Visibility(bpy.types.Panel):
    bl_label = "Bone Visibility"
    bl_idname = "CHEF_PT_Visibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = CHEF_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        boneCollections = bpy.data.armatures['ChefArmature'].collections_all

        testCol = bpy.data.armatures['ChefArmature'].collections

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
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-Face"], 'is_visible', toggle=True, text="FACE")
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Torso"], 'is_visible', toggle=True, text="TORSO")
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Torso Tweak"], 'is_visible', toggle=True, text="TORSO TWEAK")

        column.separator(factor = 1.5, type='LINE')
        
        #Arms
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Arm.L"], 'is_visible', toggle=True, text="FK-ARM.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Arm.R"], 'is_visible', toggle=True, text="FK-ARM.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Arm.L"], 'is_visible', toggle=True, text="IK-ARM.L", icon = "CON_KINEMATIC")
        row=row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Arm.R"], 'is_visible', toggle=True, text="IK-ARM.R", icon = "CON_KINEMATIC")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Hand.L"], 'is_visible', toggle=True, text="HAND.L")
        row.split(align=True)
        row.prop(boneCollections["CTRL-Hand.R"], 'is_visible', toggle=True, text="HAND.R")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Arm Tweak"], 'is_visible', toggle=True, text="ARM TWEAK")

        column.separator(factor=1.5, type='LINE')

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Accessory"], 'is_visible', toggle=True, text="ACCESSORY")


################################ Snapping ################################
class CHEF_OP_SNAP_MASTER(bpy.types.Operator):
    bl_idname = "chef.snap_master"
    bl_label = ""
    bl_description = "Snap Arm IK/FK"
    bl_options = {'UNDO', 'INTERNAL'}

    side : bpy.props.StringProperty(name="'L' or 'R'")
    snapTo : bpy.props.StringProperty(name="'FK-IK' or 'IK-FK'")

    def execute(self, context):
        side = self.side
        snapTo = self.snapTo
        
        if(snapTo == "FK-IK"):
            FK_IK(side)
        elif(snapTo == "IK-FK"):
            IK_FK(side)

        return {"FINISHED"}

#Snap FK to IK for selected limb then switch to FK
def FK_IK(side:str):
    ctrlFKPrefix = 'CTRL-FK-'
    mchPrefix = 'MCH-SNAP-'

    rigPose = bpy.data.objects['ChefArmature'].pose
    bpy.ops.pose.select_all(action='DESELECT')

    fkBone = rigPose.bones.get(ctrlFKPrefix+'Arm.'+side)
    snapBone = rigPose.bones.get(mchPrefix+'Arm.'+side)

    fkBone.matrix = snapBone.matrix.copy()
    bpy.context.view_layer.update()

    for childBone in fkBone.children_recursive:
        if(childBone.name.startswith(ctrlFKPrefix)):
            targetBone = rigPose.bones.get(childBone.name.replace(ctrlFKPrefix, mchPrefix))

            childBone.matrix = targetBone.matrix.copy()
            bpy.context.view_layer.update()
    
    '''
    mchBone = rigPose.bones.get(mchPrefix+side)
    FKBone = rigPose.bones.get(ctrlFKPrefix+side)
    FKBone.matrix = mchBone.matrix.copy()
    bpy.context.view_layer.update()
    '''

    #Set limb to FK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'Arm.{side} FK/IK'] = 0

#Snap IK to FK for selected limb then switch to IK
def IK_FK(side:str):
    ctrlIKPrefix = 'CTRL-IK-'
    ctrlFKPrefix = 'CTRL-FK-'

    rigPose = bpy.data.objects['ChefArmature'].pose
    bpy.ops.pose.select_all(action='DESELECT')

    targetFKBone = rigPose.bones.get(ctrlFKPrefix + "Arm." + side)
    IKCTRLBone= rigPose.bones.get(ctrlIKPrefix + "Shoulder." + side)
    IKCTRLBone.matrix = targetFKBone.matrix.copy()
    bpy.context.view_layer.update()

    targetFKBone = rigPose.bones.get(ctrlFKPrefix + "Wrist." + side)
    IKCTRLBone= rigPose.bones.get(ctrlIKPrefix + "Wrist." + side)
    IKCTRLBone.matrix = targetFKBone.matrix.copy()
    bpy.context.view_layer.update()

    targetFKBone = rigPose.bones.get('MCH-SNAP-Elbow.'+side)
    IKCTRLBone= rigPose.bones.get(ctrlIKPrefix + "Elbow." + side)
    IKCTRLBone.matrix = targetFKBone.matrix.copy()
    bpy.context.view_layer.update()
    bpy.context.view_layer.update()

    #Set limb to IK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'Arm.{side} FK/IK'] = 1

class CHEF_PT_Snap_Utilities(bpy.types.Panel):
    bl_label = "Snap Utilities"
    bl_idname = "CHEF_PT_Snap Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = CHEF_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        row = column.row(align=True)
        op = row.operator("chef.snap_master", emboss=True, text="ARM.L FK > IK", icon = "SNAP_ON")
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("chef.snap_master", emboss=True, text="ARM.R FK > IK", icon = "SNAP_ON")
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("chef.snap_master", emboss=True, text="ARM.L IK > FK", icon = "SNAP_ON")
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("chef.snap_master", emboss=True, text="ARM.R IK > FK", icon = "SNAP_ON")
        op.side = 'R'
        op.snapTo = 'IK-FK'

################################ Properties ################################ 
class CHEF_PT_Properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_idname = "CHEF_PT_Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = CHEF_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class CHEF_PT_HeadProperties(bpy.types.Panel):
    bl_label = "Head Properties"
    bl_idname = "CHEF_PT_HeadProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = CHEF_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['ChefArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Head Target")
        row.split(align= True)
        row.prop(bone, '["Head Target"]', text = "", slider=True)

class CHEF_PT_ArmProperties(bpy.types.Panel):
    bl_label = "Arm Properties"
    bl_idname = "CHEF_PT_ArmProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = CHEF_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['ChefArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Arm.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Arm.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Arm.L Follow")
        row.split(align= True)
        row.prop(bone, '["Arm.L Follow"]', text = "", slider=True)

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

panels = (CHEF_PT_RigUI,
          CHEF_PT_Visibility, 
          CHEF_PT_Snap_Utilities, 
          CHEF_PT_Properties,   
          CHEF_PT_HeadProperties,                                                                                                                             
          CHEF_PT_ArmProperties,
          CHEF_OP_SNAP_MASTER
          )

register, unregister = bpy.utils.register_classes_factory(panels)

#Change this from "<run_path>" to "__main__" if running from inside Blender
if __name__ == "<run_path>":
   register()