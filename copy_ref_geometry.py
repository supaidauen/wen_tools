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

class crmProps(bpy.types.PropertyGroup):
  '''Class for the Properties'''

  p_change: IntProperty(name="Percent Change",
    description="Percent of change between two meshes.",
    default=100, step=1, min=0, max=100)

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
    obj = context.active_object
    return (obj and obj.type == 'MESH')

  def execute(self, context):
    crg = context.window_manager.copyrefgeometryProps

    if ob_check(self) == False:
      return {'CANCELLED'}
    else:
      process_mesh(crg.create_dup,
             crg.p_change,
             crg.create_shape_key,
             crg.selected_verts,
             crg.copy_material,
             crg.shrinkwrap)
    bpy.context.scene.update()
    return {'FINISHED'}

def ob_check(self):
  cont = bpy.context
  # Make sure only two objects are selected.
  if len(cont.selected_objects) != 2:
    self.report({'ERROR'},"Must have exactly 2 mesh objects selected")
    return(False)
  for ob in cont.selected_objects:
    if ob.type != 'MESH':
      self.report({'ERROR'},"Must have exactly 2 mesh objects selected")
      return(False)
  return(True)

def process_mesh(dup,
         p_change,
         s_key,
         s_verts,
         material,
         shrinkwrap):
  cont = bpy.context
  # Get the active object, there can only ever be 1.
  ob_act = cont.active_object
  # Set the other object as our second selection.
  for ob in cont.selected_objects:
    if ob != ob_act:
      ob_sel = ob
  if dup:
    # Make a duplicate so we preserve our previous mesh.
    scn = bpy.context.scene
    c = ob_sel
    d = c.copy()
    d.data = c.data.copy()
    scn.objects.link(d)

  if s_key:
    if ob_act.data.shape_keys == None:
      shapeKey = ob_act.shape_key_add(from_mix=False)
      shapeKey.name = "Basis"
      for vert in ob_act.data.vertices:
        shapeKey.data[vert.index].co = vert.co
    shapeKey = ob_act.shape_key_add(from_mix=False)
    shapeKey.name = ob_sel.name+".skey"

    for vert in ob_sel.data.vertices:
      shapeKey.data[vert.index].co = vert.co
    return(True)

  if material:
    set_material(ob_act,ob_sel)

  if shrinkwrap:
    ob_act_shrinkwrap = ob_act.modifiers.new("Shrinkwrap", type='SHRINKWRAP')
    ob_act_shrinkwrap.target = ob_sel
    ob_act_shrinkwrap.vertex_group = "wrap"
    ob_act_shrinkwrap.use_keep_above_surface = True

  if ob_act.data.shape_keys and s_verts:
    for ob_act_keys,ob_sel_keys in zip(ob_act.data.shape_keys.key_blocks,
                       ob_sel.data.shape_keys.key_blocks):
      ob_act_verts = ob_act_keys.data
      ob_sel_verts = ob_sel_keys.data
      move_verts(ob_act.data.vertices,ob_act_verts,ob_sel_verts,s_verts,p_change,ob_act)

  else:
    ob_act_verts = ob_act.data.vertices
    ob_sel_verts = ob_sel.data.vertices
    move_verts(ob_act_verts,ob_act_verts,ob_sel_verts,s_verts,p_change,ob_act)

def move_verts(iterable,
         ob_act_verts,
         ob_sel_verts,
         s_verts,
         p_change,
         ob_act):
  cont = bpy.context
  def do_move(v1,v2):
    v1.co.x = ((v2.co.x - v1.co.x) * p_change) + v1.co.x
    v1.co.y = ((v2.co.y - v1.co.y) * p_change) + v1.co.y
    v1.co.z = ((v2.co.z - v1.co.z) * p_change) + v1.co.z
  p_change = p_change*0.01
  if ob_act.data.shape_keys:
    for ob in bpy.context.selected_objects:
      ob.select = False
    ob_act.select = True
    bpy.ops.object.duplicate()
    for ob in cont.selected_objects:
      if ob != ob_act:
        ob_proxy = ob
    for ob in bpy.context.selected_objects:
      ob.select = False
    ob_act.select = True
    bpy.context.scene.objects.active = ob_act
    bpy.ops.object.shape_key_remove(all=True)
    for i,v1,v2 in zip(iterable,ob_act_verts,ob_sel_verts):
      if s_verts:
        if i.select:
          do_move(v1,v2)
      else:
        do_move(v1,v2)
    ob_proxy.select = True
    for i in range(0,len(ob_proxy.data.shape_keys.key_blocks)):
      if i:
        ob_proxy.active_shape_key_index = i
        bpy.ops.object.shape_key_transfer()
    for ob in bpy.context.selected_objects:
      ob.select = False
    ob_proxy.select = True
    bpy.ops.object.delete(use_global=True)
    for i in bpy.data.meshes:
      if not i.users:
        bpy.data.meshes.remove(i)
    ob_act.select = True
    bpy.context.scene.objects.active = ob_act
    return(True)
  else:
    for i,v1,v2 in zip(iterable,ob_act_verts,ob_sel_verts):
      if s_verts:
        if i.select:
          do_move(v1,v2)
      else:
        do_move(v1,v2)

  return(True)

def set_material(ob_to, ob_from):
  if not len(ob_to.material_slots) == len(ob_from.material_slots):
    for i in len(ob_from.material_slots):
      ob_to.data.materials.append(None)
  for ob_to_mat,ob_from_mat in zip(ob_to.material_slots,ob_from.material_slots):
      ob_to_mat.material = ob_from_mat.material
  return

import sys,inspect
classes = (cls[1] for cls in inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__))

def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
