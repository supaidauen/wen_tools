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

class Quick_Save(bpy.types.Operator):
  '''Save Immediately'''

  bl_idname = "wm.quick_save"
  bl_label = "Quick Save"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self, context):
    bpy.ops.wm.save_mainfile(check_existing=False, compress=True,)
    return {'FINISHED'}
