# RoR2 Rigs
Blender rigs for vanilla RoR2 survivors, intended to be used for adding custom survivor animations with [R2API.Animations](https://thunderstore.io/package/RiskofThunder/R2API_Animations/).

### This is a WIP project. I am still in the process of figuring out how all this works, and will rely on your feedback to make sure everything runs smoothly.

Please contact @bog_rtm on Discord with feedback or issues.

---

# How to use these rigs

## IMPORTANT
- **Do not change the name of the armature. It must match the name of the survivor's armature in-game.**

- **If a bone or bone collection has a prefix of "DEF", "TGT", or "MCH", do not touch it. Animate only with bones that have the "CTRL" prefix, and the PROPERTIES bone.**

- **Make sure to check the Only Deform Bones checkbox under the Armature section when exporting as an FBX.**

- **I highly suggest using the Keying or Idle actions as the starting point for your animations. I have created the necessary transform channel keys for all relevant CTRL bones and custom properties. If a transform channel you need is not keyed, you can do so manually, but be warned that touching the scale of most bones other than the CTRL-Root bone may cause jank.**

- **Please check the attached rig ui.py file for each survivor; some of them may have extra information regarding the rig.**

- **Before you begin making elaborate complex animations right off the bat, please test out a couple of simple animations first. The rigs have not had much in-game testing, so if you identify any issues, please contact me so I can make adjustments.**

- **The textures I use in the blend files are not always the same as those used in-game. Please do not use them for anything.**

## Rig UI
When opening the Blend file, execute the attached Rig_UI.py file in the text editor in order to create a rig UI panel in the sidebar. This will allow you to easily toggle the visibility of bone collections, control custom properties, and use the FK/IK snapping operations.

This has been set up to execute automatically, so please allow scripts to run on Blender startup.

![image](https://github.com/user-attachments/assets/c77e7a6d-7ac6-4c26-98ea-692bcb8cfc85)

## Custom Properties

![image](https://github.com/user-attachments/assets/44e5a5f0-8cdb-46c4-87cd-da695063fea3)

Custom properties allow you to control various rig behaviors. In order to use them in your animations, you must create a key for the property in the armature action, and create new keys at any frame you adjust that property. I have keyed all custom properties at the start of the Keying action.

## Snapping Utilities
![image](https://github.com/user-attachments/assets/85082812-84bb-4550-b083-2f138c31d076)

These buttons allow you to snap the FK and IK controllers to one another for the associated limb. Doing so will switch the limb to the kinematics type being snapped (ie, pressing the `Arm.R IK > FK` button will cause the right arm's IK bones to snap to its FK bones,
and will switch the right arm to IK). This does **not** create a keyframe in your current action, so please be aware of this.

This will not be 100% perfect when snapping IK > FK as I have not locked the axes for the IK bones. This was done in order to recreate Hopoo's idle animations.

## Export Settings

Export your rig as an FBX with the following settings:

![image](https://github.com/user-attachments/assets/b95cf02b-6dcf-4d05-be81-93d4e9801c90)
