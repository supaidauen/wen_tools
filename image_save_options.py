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

import bpy, struct, os
from bpy.props import *

class Image_Save_Options(bpy.types.Operator):
    '''Image Save Options'''
    
    bl_idname = "save.image_save_options"
    bl_label = "Image Save Options"
    bl_description = "Better Image Save Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath = StringProperty(name="File Path", description="Path where the image will be saved",maxlen=1024, default="")
    filter_folder = BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    imageFileType = bpy.props.EnumProperty(items=[('PNG Save',)]
    
    def execute(self, context):
        self.save_image()
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    def save_image(self):
        img = bpy.context.space_data.image
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        
        
        