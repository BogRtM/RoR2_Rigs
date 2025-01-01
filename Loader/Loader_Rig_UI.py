# context.area: VIEW_3D

#PLEASE READ THE README FOR A GUIDE ON HOW TO USE THIS RIG
#https://github.com/BogRtM/RoR2_Rigs
#Contact @bog_rtm on Discord for questions

#PLEASE READ THE README FOR A GUIDE ON HOW TO USE THIS RIG
#https://github.com/BogRtM/RoR2_Rigs
#Contact @bog_rtm on Discord for questions

import bpy

rig_id = "LOADER_RIG_ID"

class LOADER_PT_RigUI(bpy.types.Panel):
    bl_label = "Rig UI"
    bl_idname = "VIEW3D_PT_Loader_RigUI"
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
class LOADER_PT_Visibility(bpy.types.Panel):
    bl_label = "Bone Visibility"
    bl_idname = "LOADER_PT_Visibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        boneCollections = bpy.data.armatures['LoaderArmature'].collections_all

        testCol = bpy.data.armatures['LoaderArmature'].collections

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
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Shoulders"], 'is_visible', toggle=True, text="SHOULDERS")

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
        row.prop(boneCollections["CTRL-Fingers.L"], 'is_visible', toggle=True, text="FINGERS.L")
        row.split(align=True)
        row.prop(boneCollections["CTRL-Fingers.R"], 'is_visible', toggle=True, text="FINGERS.R")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Arm Tweak"], 'is_visible', toggle=True, text="ARM TWEAK")

        column.separator(factor=1.5, type='LINE')

        #Gauntlet
        row = column.row(align=True)
        row.prop(boneCollections["CTRL-FK-Gauntlet.L"], 'is_visible', toggle=True, text="FK-GAUNTLET.L", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        row = row.split(align=True)
        row.prop(boneCollections["CTRL-FK-Gauntlet.R"], 'is_visible', toggle=True, text="FK-GAUNTLET.R", icon = "DRIVER_ROTATIONAL_DIFFERENCE")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-IK-Gauntlet.L"], 'is_visible', toggle=True, text="IK-GAUNTLET.L", icon = "CON_KINEMATIC")
        row=row.split(align=True)
        row.prop(boneCollections["CTRL-IK-Gauntlet.R"], 'is_visible', toggle=True, text="IK-GAUNTLET.R", icon = "CON_KINEMATIC")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Gauntlet Fingers.L"], 'is_visible', toggle=True, text="GAUNTLET FINGERS.L")
        row.split(align=True)
        row.prop(boneCollections["CTRL-Gauntlet Fingers.R"], 'is_visible', toggle=True, text="GAUNTLET FINGERS.R")

        row = column.row(align=True)
        row.prop(boneCollections["CTRL-Mech Base"], 'is_visible', toggle=True, text="MECH BASE")

        column.separator(factor=1.5, type='LINE')

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

        column.separator(factor=1.5, type='LINE')


################################ Snapping ################################
class LOADER_OP_SNAP_MASTER(bpy.types.Operator):
    bl_idname = "loader.snap_master"
    bl_label = ""
    bl_description = "Snap Arm IK/FK"
    bl_options = {'UNDO', 'INTERNAL'}

    limb : bpy.props.StringProperty(name="'Arm' or 'Leg' or 'Gauntlet'")
    side : bpy.props.StringProperty(name="'L' or 'R'")
    snapTo : bpy.props.StringProperty(name="'FK-IK' or 'IK-FK'")

    def execute(self, context):
        limb = self.limb
        side = self.side
        snapTo = self.snapTo
        
        if(snapTo == "FK-IK"):
            FK_IK(limb, side)
        elif(snapTo == "IK-FK"):
            IK_FK(limb, side)

        return {"FINISHED"}

#Snap FK to IK for selected limb then switch to FK
def FK_IK(limb:str, side:str):
    ctrlFKPrefix = 'CTRL-FK-'
    mchPrefix = 'MCH-IK-'
    side = side.lower()

    print("Snapping " + limb + "." + side + " FK to IK")

    rigPose = bpy.data.objects['LoaderArmature'].pose
    bpy.ops.pose.select_all(action='DESELECT')

    match limb:
        case "Arm":
            chainLink = "upper_arm."
        case "Leg":
            chainLink = "thigh."
        case "Gauntlet":
            chainLink = "mech.upper_arm."
    
    mchBone = rigPose.bones.get(mchPrefix+chainLink+side)
    FKBone = rigPose.bones.get(ctrlFKPrefix+chainLink+side)
    FKBone.matrix = mchBone.matrix.copy()
    bpy.context.view_layer.update()

    match limb:
        case "Arm":
            chainLink = "lower_arm."
        case "Leg":
            chainLink = "calf."
        case "Gauntlet":
            chainLink = "mech.lower_arm."

    mchBone = rigPose.bones.get(mchPrefix + chainLink + side)
    FKBone = rigPose.bones.get(ctrlFKPrefix + chainLink + side)
    FKBone.matrix = mchBone.matrix.copy()
    bpy.context.view_layer.update()

    match limb:
        case "Arm":
            chainLink = "hand."
        case "Leg":
            chainLink = "foot."
        case "Gauntlet":
            chainLink = "mech.hand."

    mchBone = rigPose.bones.get(mchPrefix + chainLink + side)
    FKBone = rigPose.bones.get(ctrlFKPrefix + chainLink + side)

    try:
        FKBone.matrix = mchBone.matrix.copy()
        bpy.context.view_layer.update()
    except:
        print(mchPrefix + chainLink + side)
        print(ctrlFKPrefix + chainLink + side)

    if(limb == "Leg"):
        chainLink = "toe."

        mchBone = rigPose.bones.get("CTRL-IK-" + chainLink + side)
        FKBone = rigPose.bones.get(ctrlFKPrefix + chainLink + side)
        FKBone.matrix = mchBone.matrix.copy()
        bpy.context.view_layer.update()
        

    #Set limb to FK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb}.{side.upper()} FK/IK'] = 0

#Snap IK to FK for selected limb then switch to IK
def IK_FK(limb:str, side:str):
    ctrlIKPrefix = 'CTRL-IK-'
    mchSnapPrefix = 'MCH-SNAP-IK-'
    side = side.lower()

    IKBoneString:str
    poleBoneString:str

    print("Snapping " + limb + "." + side + " IK to FK")

    rigPose = bpy.data.objects['LoaderArmature'].pose
    bpy.ops.pose.select_all(action='DESELECT')

    match limb:
        case "Arm":
            IKBoneString = "hand."
            poleBoneString = "Elbow."
        case "Leg":
            IKBoneString = "FootMaster."
            poleBoneString = "Knee."
        case "Gauntlet":
            IKBoneString = "Gauntlet."
            poleBoneString = "GauntletElbow."

    mchSnapBone = rigPose.bones.get(mchSnapPrefix + IKBoneString + side)
    IKCTRLBone= rigPose.bones.get(ctrlIKPrefix + IKBoneString + side)
    IKCTRLBone.matrix = mchSnapBone.matrix.copy()
    bpy.context.view_layer.update()

    mchPoleSnapBone = rigPose.bones.get(mchSnapPrefix + poleBoneString + side)
    poleCTRLBone = rigPose.bones.get(ctrlIKPrefix + poleBoneString + side)
    poleCTRLBone.matrix = mchPoleSnapBone.matrix.copy()
    bpy.context.view_layer.update()

    if(limb == "Leg"):
        chainLink = "toe."

        mchBone = rigPose.bones.get("CTRL-FK-" + chainLink + side)
        toeBone = rigPose.bones.get("CTRL-IK-" + chainLink + side)
        toeBone.matrix = mchBone.matrix.copy()
        bpy.context.view_layer.update()

    #Set limb to IK
    propBone = rigPose.bones.get("PROPERTIES")
    propBone[f'{limb}.{side.upper()} FK/IK'] = 1

class LOADER_PT_Snap_Utilities(bpy.types.Panel):
    bl_label = "Snap Utilities"
    bl_idname = "LOADER_PT_Snap Utilities"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        column = layout.column()

        #Arms
        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="ARM.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="ARM.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="ARM.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="ARM.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Arm'
        op.side = 'R'
        op.snapTo = 'IK-FK'

        column.separator(factor=1.5, type = 'LINE')

        #Gauntlets
        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="GAUNTLET.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Gauntlet'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="GAUNTLET.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Gauntlet'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="GAUNTLET.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Gauntlet'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="GAUNTLET.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Gauntlet'
        op.side = 'R'
        op.snapTo = 'IK-FK'

        column.separator(factor=1.5, type = 'LINE')

        #Legs
        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="LEG.L FK > IK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'L'
        op.snapTo = 'FK-IK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="LEG.R FK > IK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'R'
        op.snapTo = 'FK-IK'

        row = column.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="LEG.L IK > FK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'L'
        op.snapTo = 'IK-FK'
        row = row.row(align=True)
        op = row.operator("Loader.snap_master", emboss=True, text="LEG.R IK > FK", icon = "SNAP_ON")
        op.limb = 'Leg'
        op.side = 'R'
        op.snapTo = 'IK-FK'

################################ Properties ################################ 
class LOADER_PT_Properties(bpy.types.Panel):
    bl_label = "Properties"
    bl_idname = "LOADER_PT_Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_RigUI.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

class LOADER_PT_HeadProperties(bpy.types.Panel):
    bl_label = "Head Properties"
    bl_idname = "LOADER_PT_HeadProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout    
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['LoaderArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Head Target")
        row.split(align= True)
        row.prop(bone, '["Head Target"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Head Follow")
        row.split(align= True)
        row.prop(bone, '["Head Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Neck Follow")
        row.split(align= True)
        row.prop(bone, '["Neck Follow"]', text = "", slider=True)

class LOADER_PT_GauntletProperties(bpy.types.Panel):
    bl_label = "Gauntlet Properties"
    bl_idname = "LOADER_PT_GauntletProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout    
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['LoaderArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Gauntlet.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Gauntlet.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Gauntlet.L Follow")
        row.split(align= True)
        row.prop(bone, '["Gauntlet.L Follow"]', text = "", slider=True)

        box = layout.box()
        column = box.column()

        row = column.row(align=True)
        row.label(text = "Gauntlet.R FK/IK")
        row.split(align= True)
        row.prop(bone, '["Gauntlet.R FK/IK"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Gauntlet.R Follow")
        row.split(align= True)
        row.prop(bone, '["Gauntlet.R Follow"]', text = "", slider=True)
        

class LOADER_PT_ArmProperties(bpy.types.Panel):
    bl_label = "Arm Properties"
    bl_idname = "LOADER_PT_ArmProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['LoaderArmature'].pose.bones['PROPERTIES']

        row = column.row(align=True)
        row.label(text = "Arm.L FK/IK")
        row.split(align= True)
        row.prop(bone, '["Arm.L FK/IK"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Arm.L Follow")
        row.split(align= True)
        row.prop(bone, '["Arm.L Follow"]', text = "", slider=True)

        row = column.row(align=True)
        row.label(text = "Arm.L Hold Handle")
        row.split(align= True)
        row.prop(bone, '["Arm.L Hold Handle"]', text = "", slider=True)
        
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
        row.label(text = "Arm.R Hold Handle")
        row.split(align= True)
        row.prop(bone, '["Arm.R Hold Handle"]', text = "", slider=True)
        
        row = column.row(align=True)
        row.label(text = "Arm.R IK Stretch")
        row.split(align= True)
        row.prop(bone, '["Arm.R IK Stretch"]', text = "", slider=True)

class LOADER_PT_LegProperties(bpy.types.Panel):
    bl_label = "Leg Properties"
    bl_idname = "LOADER_PT_LegProperties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"
    bl_parent_id = LOADER_PT_Properties.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        column = box.column()

        bone = bpy.data.objects['LoaderArmature'].pose.bones['PROPERTIES']

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

panels = (LOADER_PT_RigUI,
          LOADER_PT_Visibility, 
          LOADER_PT_Snap_Utilities, 
          LOADER_PT_Properties,
          LOADER_PT_HeadProperties,
          LOADER_PT_GauntletProperties,
          LOADER_PT_ArmProperties,
          LOADER_PT_LegProperties,
          LOADER_OP_SNAP_MASTER
          )

register, unregister = bpy.utils.register_classes_factory(panels)
#def register():
 #   bpy.utils.register_class(LOADER_PT_RigUI)
        
#def unregister():
#    bpy.utils.unregister_class(LOADER_PT_RigUI)

if __name__ == "__main__":
   register()