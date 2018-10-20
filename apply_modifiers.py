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
from bpy.props import BoolProperty

C = bpy.context

class aamProps(bpy.types.PropertyGroup):
  '''Class for the properties'''
  
  dodup = BoolProperty(name="Duplicate Objects",
  description="Duplicate the Objects",
  default=True)
  
  showv = BoolProperty(name="Un-Hide Modifiers",
  description="Un-Hide hidden Modifiers",
  default=True)
  
  applym = BoolProperty(name="Apply Modifiers",
  description="Apply the Modifiers",
  default=True)

class Apply_Modifiers(bpy.types.Operator):
  '''Apply All Modifiers'''
  
  bl_idname = "object.apply_modifiers"
  bl_label = "Apply All Modifiers"
  bl_options = {'REGISTER', 'UNDO'}
  
  @classmethod
  def poll(self, context):
    obj = context.active_object
    return (obj and obj.type == 'MESH')
  
  def draw(self, context):
    aam = context.window_manager.applymodifiersProps
    layout = self.layout
    row = self.layout.row(align=True)
    row.prop(crg, "dodup", text='Duplicate Objects')
    row = self.layout.row(align=True)
    row.prop(crg, "showv", text='Un-Hide Modifiers')
    row = self.layout.row(align=True)
    row.prop(crg, "dodup", text='Apply Modifiers')
    
    
  def execute(self, context):
    aap = context.window_manager.applymodifiersProps
    apply_mods(aap.dodup,aap.showv,aap.applym)
    return {'FINISHED'}
    
def apply_mods(dodup,showv,applym):
  if dodup:
    bpy.ops.object.duplicate()
  displaymods(showv)
  if applym:
    for ob in C.selected_objects:
      C.scene.objects.active = ob
      for mod in ob.modifiers:
        bpy.ops.object.modifier_apply(apply_as='DATA',modifier=mod.name)
    return True
  else:
    return True

def displaymods(showv):
  for ob in C.selected_objects:
     for mod in ob.modifiers:
       if mod.name != 'Armature':
         mod.show_viewport = showv
         
