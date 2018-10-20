# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import EnumProperty
from bpy import ops
from bpy_extras.io_utils import ExportHelper, axis_conversion
from mathutils import Vector, Matrix
from io_scene_fbx import export_fbx_bin
from io_scene_obj import export_obj

def do_fbx_export(self,actions):
  context = bpy.context
  forward = 'Y'
  up = 'Z'

  export_fbx_bin.save_single(self, context.scene, self.filepath,context_objects=context.selected_objects,
  axis_forward = forward,
  axis_up = up,
  version = 'BIN7400',
  ui_tab = 'MAIN',
  use_selection = True,
  global_scale = 1.0,
  apply_unit_scale = True,
  bake_space_transform = False,
  object_types = {'MESH', 'ARMATURE'},
  use_mesh_modifiers = True,
  mesh_smooth_type = 'OFF',
  use_mesh_edges = True,
  use_tspace = True,
  use_custom_props = False,
  add_leaf_bones = False,
  primary_bone_axis = 'Y',
  secondary_bone_axis = 'X',
  use_armature_deform_only = False,
  bake_anim = actions,
  bake_anim_use_all_bones = actions,
  bake_anim_use_nla_strips = actions,
  bake_anim_use_all_actions = actions,
  bake_anim_force_startend_keying = actions,
  bake_anim_step = 1.0,
  bake_anim_simplify_factor = 0.0,
  use_anim = actions,
  use_anim_action_all = actions,
  use_default_take = actions,
  use_anim_optimize = actions,
  anim_optimize_precision = 6.0,
  path_mode = 'AUTO',
  embed_textures = False,
  batch_mode = 'OFF',
  use_batch_own_dir = True)

def do_obj_export(self):

  bpy.ops.export_scene.obj(#context,
  filepath=self.filepath,
  axis_forward='-Z',
  axis_up='Y',
  filter_glob="*.obj",
  use_triangles=True,
  use_edges=False,
  use_normals=True,
  use_smooth_groups=False,
  use_smooth_groups_bitflags=False,
  use_uvs=True,
  use_materials=False,
  use_mesh_modifiers=True,
  use_blen_objects=True,
  group_by_object=False,
  group_by_material=False,
  keep_vertex_order=True,
  use_vertex_groups=False,
  use_nurbs=False,
  use_selection=True,
  use_animation=False,
  #global_matrix=None,
  path_mode='AUTO')

def do_obj_import(self):

  bpy.ops.import_scene.obj(#context,
  filepath=self.filepath,
  axis_forward='-Z',
  axis_up='Y',
  filter_glob="*.obj",
  use_edges=False,
  use_smooth_groups=False,
  split_mode="ON")

class Export_SM_to_UE4(bpy.types.Operator, ExportHelper):
  '''Export to UE4'''

  bl_idname = "object.export_sm_to_ue4"
  bl_label = "Export to UE4"
  bl_options = {'REGISTER', 'UNDO'}
  filename_ext = ".fbx"

  @classmethod
  def poll(self, context):
    obj = context.active_object
    if hasattr(obj, "type"):
      return (obj and obj.type == 'MESH' or "ARMATURE")

  def execute(self, context):
    cont = bpy.context
    data = bpy.data
    scn = cont.scene
    if len(bpy.context.selected_objects) == 1 and \
      bpy.context.selected_objects[0].type == "ARMATURE" and \
      len(bpy.context.selected_objects[0].children) == 0:
      do_fbx_export(self,False)
      return {'FINISHED'}
    obs = cont.active_object.children
    layers = []
    old_arm = bpy.context.active_object
    ue4_arm = bpy.data.objects['ROOT'] if 'ROOT' in bpy.data.objects else old_arm

    if ue4_arm == '':
      self.report({'ERROR'}, "No Valid Armatures for export, please assign an Armature parent relationship, aborting.")
      return {'CANCELLED'}

    for ob in obs:
      old_parent = ob.parent
      ob.parent = ue4_arm
      ob.select = True

    for i in range(len(scn.layers)):
      if ue4_arm.layers[i] == True:
        if old_arm.layers[i] == False:
          bpy.context.scene.layers[i] = True
          layers.append(i)

    ue4_arm.select = True
    bpy.context.scene.objects.active = ue4_arm
    if "act.rest_pose" in bpy.data.actions:
      bpy.context.active_object.animation_data.action = bpy.data.actions["act.rest_pose"]
    
    bpy.context.scene.update()

    do_fbx_export(self,False)

    for ob in obs:
      ob.parent = old_parent
      ob.select = True

    if ue4_arm != old_arm:
      ue4_arm.select = False
      old_arm.select = True

    for i in layers:
      bpy.context.scene.layers[i] = False

    bpy.context.scene.update()
    return {'FINISHED'}

class Export_OBJ_to_BAKER(bpy.types.Operator, ExportHelper):
  '''Export Obj'''

  bl_idname = "object.export_obj_quick"
  bl_label = "Export Obj"
  bl_options = {'REGISTER', 'UNDO'}
  filename_ext = ".obj"

  @classmethod
  def poll(self, context):
    obj = context.active_object
    if hasattr(obj, "type"):
      return (obj and obj.type == 'MESH')

  def execute(self, context):

    do_obj_export(self)

    return {'FINISHED'}


class Import_OBJ_for_CAGE(bpy.types.Operator, ExportHelper):
  '''Import Obj'''

  bl_idname = "object.import_obj_quick"
  bl_label = "Import Obj"
  bl_options = {'REGISTER', 'UNDO'}
  filename_ext = ".obj"

  def execute(self, context):

    do_obj_import(self)

    return {'FINISHED'}

class Bake_Animations(bpy.types.Operator, ExportHelper):
  '''Bake Deform Animation'''

  bl_idname = "object.bake_deform_animations"
  bl_label = "Bake UE4 Animations"
  bl_options = {'REGISTER', 'UNDO'}
  filename_ext = ".fbx"

  @classmethod
  def poll(self, context):
    obj = context.active_object
    if hasattr(obj, "type"):
      return(obj and obj.type == 'ARMATURE')

  def execute(self, context):
    keyframes = []
    layers = []
    arm = bpy.context.active_object
    current_anim = bpy.context.active_object.animation_data.action
    ue4_arm = bpy.data.objects['ROOT']

    bpy.ops.pose.select_all(action='DESELECT')
    arm.pose.bone_groups.active = arm.pose.bone_groups['Pose_Bones']
    bpy.ops.pose.group_select()

    for f in bpy.context.active_object.animation_data.action.fcurves:
      for keyframe in f.keyframe_points:
        x, y = keyframe.co
        if x not in keyframes:
          keyframes.append(int(x))


    for i in keyframes:
      bpy.context.scene.frame_set(i)
      bpy.ops.anim.keyframe_insert_menu(type='__ACTIVE__', confirm_success=True)

    bpy.context.scene.frame_set(keyframes[0])

    for i in range(0,20):
      if ue4_arm.layers[i] == True:
        bpy.context.scene.layers[i] = True
        layers.append(i)

    bpy.context.scene.objects.active = ue4_arm
    arm.select = False
    ue4_arm.select = True
    bpy.context.active_object.animation_data.action = current_anim

    do_fbx_export(self,True)

    for i in layers:
      bpy.context.scene.layers[i] = False

    bpy.context.scene.objects.active = arm

    return { 'FINISHED' }
