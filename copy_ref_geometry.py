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
from bpy.props import IntProperty,BoolProperty

class CRM_Props(bpy.types.PropertyGroup):
  '''Class for the Properties'''

  p_change: IntProperty(name="Amount Change",
    description="Amount of change between two meshes.",
    default=1, step=0.01, min=0, max=1)

  selected_verts: BoolProperty(name="Only Selected",
    description="Use only selected verts.",
    default=False)

  create_dup: BoolProperty(name="Create Dup",
    description="Creates a duplicate of the active object.",
    default=False)

  create_shape_key: BoolProperty(name="Create Shape Key",
    description="Creates a shape key in the active object of the selected object.",
    default=False)

  copy_material: BoolProperty(name="Copy Material",
    description="Copies the Selected objects material onto the Active or the Duplicate.",
    default=False)

  shrinkwrap: BoolProperty(name="Shrinkwrap",
    description="Shrinkwraps unaffected vertices.",
    default=False)

class OBJECT_OT_Copy_Reference_Mesh_Geometry(bpy.types.Operator):
  '''Copy Reference Mesh Geometry.  Meshes Must have similar topology'''

  bl_idname = "object.copy_vert_loc_from_ref"
  bl_label = "Copy Reference Mesh"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    ob = context.active_object
    return (ob and ob.type == 'MESH')

  def execute(self, context):
    crg = context.scene.copyrefgeometryProps
    cont = bpy.context
  # Make sure only two objects are selected.
    if len(cont.selected_objects) != 2:
      self.report({'ERROR'},"Must have exactly 2 mesh objects selected")
      return{'CANCELLED'}
    for ob in cont.selected_objects:
      if ob.type != 'MESH':
        self.report({'ERROR'},"Must have exactly 2 mesh objects selected")
        return{'CANCELLED'}
    # Get the active object, there can only ever be 1.
    ob_act = cont.active_object
    # Set the other object as our second selection.
    ob_sel = [ob for ob in cont.selected_objects if ob is not ob_act][0]

    if dup:
      ob_act.select_set(False)
      # Make a duplicate so we preserve our previous mesh.
      ob_temp = ob_act.copy()
      ob_temp.name = ob_act.name+"_dup"
      ob_temp.data = ob_act.data.copy()
      ob_temp.data.name = ob_act.data.name+"_dup"
      C.view_layer.active_layer_collection.collection.objects.link(ob_temp)
      ob_temp.select_set(True)
      bpy.context.view_layer.objects.active = ob_act = new_object

    if s_key:
      if ob_act.data.shape_keys == None:
        shapeKey = ob_act.shape_key_add(from_mix=False)
        shapeKey.name = "Basis"
        for v in ob_act.data.vertices:
          shapeKey.data[v.index].co = vert.co
      shapeKey = ob_act.shape_key_add(from_mix=False)
      shapeKey.name = ob_sel.name+".skey"
      return(True)

    if material:
      if not len(ob_to.material_slots) == len(ob_from.material_slots):
      for i in len(ob_from.material_slots):
        ob_to.data.materials.append(None)
      for i in range(len(ob_to.material_slots)):
          mat.material = ob_from.data.materials[i]

    if shrinkwrap:
      ob_act_shrinkwrap = ob_act.modifiers.new("Shrinkwrap", type='SHRINKWRAP')
      ob_act_shrinkwrap.target = ob_sel
      ob_act_shrinkwrap.vertex_group = "wrap"
      ob_act_shrinkwrap.use_keep_above_surface = True

    if ob_act.data.shape_keys:
      verts = ob_act.active_shape_key.data
    else:
      verts = ob_act.data.vertices

    for v in ob_act.data.vertices:
      if s_verts:
        if not v.select_get():
          continue
      co = verts[v.index].co
      co_trans = ob_sel.data.vertices[v.index]
      co.x = ((co_trans.co.x - co.x) * p_change) + co.x
      co.y = ((co_trans.co.y - co.y) * p_change) + co.y
      co.z = ((co_trans.co.z - co.z) * p_change) + co.z

    bpy.context.view_layer.update()
    return {'FINISHED'}

classes = (
OBJECT_OT_Copy_Reference_Mesh_Geometry,
CRM_Props,
)

def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
