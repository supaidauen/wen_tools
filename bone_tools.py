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
from bpy.utils import register_class

def get_bones(arm, context, selected):
  """
  Get armature bones according to current context

    get_bones(bpy.data.armature, bpy.context, boolean)

  returns list

    [bpy_types.Bone]
  """
  if context.mode == 'EDIT_ARMATURE':
    if selected:
      bones = context.selected_bones
    else:
      bones = arm.edit_bones
  elif context.mode == 'OBJECT':
    if selected:
      bones = []
    else:
      bones = arm.bones
  else:
    if selected:
      pose_bones = context.selected_pose_bones
      bones = [arm.bones[b.name] for b in pose_bones]
    else:
      bones = arm.bones

  return bones

def check_used_layer(arm, layer_idx, context):
  """
  Check wether the given layer is used
  """
  bones = get_bones(arm, context, False)

  is_use = 0

  for bone in bones:
    if bone.layers[layer_idx]:
      is_use = 1
      break

  return is_use

def check_selected_layer(arm, layer_idx, context):
  """
  Check wether selected bones are in layer
  """
  bones = get_bones(arm, context, True)

  is_sel = 0

  for bone in bones:
    if bone.layers[layer_idx]:
      is_sel = 1
      break

  return is_sel

class OBJECT_OT_Pose_Rest_Toggle(bpy.types.Operator):
  '''Pose/Rest Toggle'''

  bl_idname = "pose.pose_rest_toggle"
  bl_label = "Pose/Rest Toggle"
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    cont = bpy.context
    if cont.active_object.data.pose_position == 'POSE': cont.active_object.data.pose_position = 'REST'
    else: cont.active_object.data.pose_position = 'POSE'
    return {'FINISHED'}

class VIEW_3D_PT_Bone_Tools(bpy.types.Panel):
  '''Bone Tools Panel'''

  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_label = "Bone Tools Panel"

  @classmethod
  def poll(cls, context):
    return context.mode in {'POSE','EDIT_ARMATURE'}

  def draw(self, context):
    layout = self.layout
    box = layout.box()
    column = box.column(align = True)
    column.label("Bone Layers:")
    row = column.row(align=True)
    row.alignment = 'EXPAND'
    row.prop(context.active_object.data, "layers", toggle=True, text='')
    row = column.row(align=True)

classes = (
  OBJECT_OT_Pose_Rest_Toggle,
  VIEW_3D_PT_Bone_Tools
)
register, unregister = bpy.utils.register_classes_factory(classes)
