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
from bpy.props import StringProperty


def prep_hair_uv(translate):
  last_area = bpy.context.area.type
  bpy.context.area.type = 'IMAGE_EDITOR'

  bpy.ops.uv.select_all(action='SELECT')

  # you need to make sure here, that object is in edit mode and UVs are selected or it will crash!

  bpy.ops.transform.rotate(value=1.5708, axis=(-0, -0, -1))
  bpy.ops.transform.resize(value=(0.333, 0.9, 1))
  if type != None:
    bpy.ops.transform.translate(value=(translate, 0, 0), 
     constraint_axis=(True, False, False))
  bpy.ops.transform.translate(value=(0, 0.04, 0), 
   constraint_axis=(False, True, False))
  bpy.context.area.type = last_area
  return

def prep_hair_movement():
  bpy.context.active_object.data.use_paint_mask_vertex = True
  bpy.ops.paint.weight_gradient(type='LINEAR', xstart=1151, xend=617, ystart=114, yend=793)
  bpy.ops.object.vertex_group_smooth(factor=0.3, repeat=30, expand=0.6)
  return

def prep_hair_object():
  def make_mesh(ob):
    scn = bpy.context.scene
    me = ob.to_mesh(scn, True, 'PREVIEW')
    o = bpy.data.objects.new(ob.name, me)
    scn.objects.link(o)
    o.matrix_world = ob.matrix_world
    o.select = True
    bpy.context.scene.objects.active = o
    return 

  for ob in bpy.context.selected_objects:
    make_mesh(ob)
    ob.select = False
  return

class phProps(bpy.types.PropertyGroup):
  '''Class for the Properties'''

  hair_material_prefix: StringProperty(name="Hair Material Prefix",
    description="Hair Material Prefix.",
    default='hair')

  hair_export_object: StringProperty(name="Hair Export Object",
    description="Name of Hair Export Object.",
    default='HairNew')

class OBJECT_OT_Prep_Hair_Movement(bpy.types.Operator):
  '''Prepare Hair Movement'''

  bl_idname = "object.prep_hair_movement"
  bl_label = "Prepare Hair Movement"
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self, context):
    prep_hair_movement()
    return {'FINISHED'}

class OBJECT_OT_Prep_Hair_Object(bpy.types.Operator):
  '''Prepare Hair Object'''

  bl_idname = "object.prep_hair_object"
  bl_label = "Prepare Hair Object"
  bl_options = {'REGISTER', 'UNDO'}

  hair_type_list = ["Thick","Mid","Thin"]
  hair_material_prefix: StringProperty(name='Hair Material Prefix', default='hair')
  hair_export_object: StringProperty(name='Hair Export Object', default='HairNew')

  def execute(self, context):
    hair_bodies = []
    for i in self.hair_type_list:
      hair_material_index = self.hair_type_list.index(i)
      hair_material_suffix = str(hair_material_index).zfill(3)
      for ob in bpy.data.objects:
        ob.select = False
        if ob.active_material and ob.active_material.name == self.hair_material_prefix+"."+hair_material_suffix:
          ob.select = True
      if not len(bpy.context.selected_objects):
        continue
      prep_hair_object()
      bpy.ops.apply.transformlocrotscale(option='SCALE')
      bpy.ops.object.join()
      hair = bpy.context.active_object
      hair_bodies.append(hair)
      vg = hair.vertex_groups.new("head")
      for v in hair.data.vertices:
        v.select = True
        vg.add([v.index], 1.0, "ADD")
      vg = hair.vertex_groups.new(i)
      for v in hair.data.vertices:
        v.select = True
        vg.add([v.index], 1.0, "ADD")
      bpy.ops.object.mode_set(mode='EDIT')
      prep_hair_uv((hair_material_index-1)*0.333)
      bpy.ops.object.mode_set(mode='OBJECT')
    for hair in hair_bodies:
      hair.select = True
    bpy.ops.object.join()
    hair = bpy.context.active_object
    hair.data.materials.clear()
    hair.name = "_HairNew_"
    hair.layers[1] = True
    hair.layers[0] = False
    scn = bpy.context.scene
    scn.layers = hair.layers
    hair_export = bpy.data.objects[self.hair_export_object]
    bpy.context.scene.objects.active = hair_export
    for ob in bpy.data.objects:
      ob.select = False
    hair_export.select = True
    bpy.ops.object.clear_mesh()
    hair.select = True
    bpy.ops.object.join()
    return {'FINISHED'}

import sys,inspect
classes = (
OBJECT_OT_Prep_Hair_Movement,
OBJECT_OT_Prep_Hair_Object,
phProps,
)

def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
