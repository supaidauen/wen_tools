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
from bpy.types import Menu

bl_info = {
  'name': 'Pie Brushes',
  'author': 'Wen',
  'version': (0,6),
  'blender': (2, 5, 6),
  'location': 'View3D > Object',
  'description': 'Pie Menus for Brushes',
  'warning': '', # used for warning icon and text in addons panel
  'wiki_url': '',
  'tracker_url': '',
  'category': '3D View'}

__bpydoc__ = '''
Pie Menus for Brushes
'''

class VIEW3D_PIE_Brushes(Menu):
  '''Pie Menus for Brushes'''

  bl_idname = "paint.pie_brush"
  bl_label = "Brushes Pie"
  bl_options = {'REGISTER', 'UNDO'}
  def draw(self, context):
    
    if bpy.context.mode == 'SCULPT':
      layout = self.layout
      pie = layout.menu_pie()
      row = pie.split().column(align=True)
      row.operator('paint.brush_select', text='Blob', icon='BRUSH_BLOB').sculpt_tool = 'BLOB'
      row.operator('paint.brush_select', text='Clay', icon='BRUSH_CLAY').sculpt_tool = 'CLAY'
      row.operator('paint.brush_select', text='Clay Strips', icon='BRUSH_CLAY_STRIPS').sculpt_tool = 'CLAY_STRIPS'
      row.operator('paint.brush_select', text='Crease', icon='BRUSH_CREASE').sculpt_tool = 'CREASE'
      row.operator('paint.brush_select', text='Draw', icon='BRUSH_SCULPT_DRAW').sculpt_tool = 'DRAW'
      row.operator('paint.brush_select', text='Layer', icon='BRUSH_LAYER').sculpt_tool = 'LAYER'
      row.operator('paint.brush_select', text='Inflate', icon='BRUSH_INFLATE').sculpt_tool = 'INFLATE'
      row = pie.split().column(align=True)
      row.operator('paint.brush_select', text='Fill', icon='BRUSH_FILL').sculpt_tool = 'FILL'
      row.operator('paint.brush_select', text='Flatten', icon='BRUSH_FLATTEN').sculpt_tool = 'FLATTEN'
      row.operator('paint.brush_select', text='Pinch', icon='BRUSH_PINCH').sculpt_tool = 'PINCH'
      row.operator('paint.brush_select', text='Mask', icon='BRUSH_MASK').sculpt_tool = 'MASK'
      row.operator('paint.brush_select', text='Scrape', icon='BRUSH_SCRAPE').sculpt_tool = 'SCRAPE'
      row.operator('paint.brush_select', text='Smooth', icon='BRUSH_SMOOTH').sculpt_tool = 'SMOOTH'
      row = pie.split().column(align=True)
      row.operator('paint.brush_select', text='Grab', icon='BRUSH_GRAB').sculpt_tool = 'GRAB'
      row.operator('paint.brush_select', text='Rotate', icon='BRUSH_ROTATE').sculpt_tool = 'ROTATE'
      row.operator('paint.brush_select', text='Nudge', icon='BRUSH_NUDGE').sculpt_tool = 'NUDGE'
      row.operator('paint.brush_select', text='Snake Hook', icon='BRUSH_SNAKE_HOOK').sculpt_tool = 'SNAKE_HOOK'
      row.operator('paint.brush_select', text='Thumb', icon='BRUSH_THUMB').sculpt_tool = 'THUMB'
    elif bpy.context.mode == 'PAINT_TEXTURE':
      layout = self.layout
      pie = layout.menu_pie()
      row = pie.split().column(align=True)
      row.operator('paint.brush_select', text='Draw', icon='BRUSH_TEXDRAW').texture_paint_tool = 'DRAW'
      row.operator('paint.brush_select', text='Soften', icon='BRUSH_SOFTEN').texture_paint_tool = 'SOFTEN'
      row.operator('paint.brush_select', text='Smear', icon='BRUSH_SMEAR').texture_paint_tool = 'SMEAR'
      row.operator('paint.brush_select', text='Fill', icon='BRUSH_TEXFILL').texture_paint_tool = 'FILL'
      row.operator('paint.brush_select', text='Mask', icon='BRUSH_TEXMASK').texture_paint_tool = 'MASK'
   