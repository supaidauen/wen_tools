# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
  'name': 'Wen Tools',
  'author': 'Supaidauen',
  'version': (21, 11 ,2018),
  'blender': (2, 80, 0),
  'location': 'View3D > Object',
  'description': 'Tools and keymaps to aid in content/character creation',
  'warning': '', # used for warning icon and text in addons panel
  'wiki_url': '',
  'tracker_url': '',
  'category': 'Object'}

bpydoc = '''Tools and keymaps to aid in content/character creation'''

import importlib

libs = (
  ".basic_ops",
  ".copy_ref_geometry",
  ".mesh_hair_tools",
  ".ue4_tools",
)

if not 'bpy' in locals():
  modules = []
  import bpy
  for lib in libs:
    i = importlib.import_module(lib, package="wen_tools")
    modules.append(i)
    i.register()
else:
  for i in modules:
    importlib.reload(i)
    i.unregister()

class VIEW_3D_PT_WenToolsPanel(bpy.types.Panel):
  '''Wen Tools Panel'''

  bl_label = "Wen Tools"
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "View"


  @classmethod
  def poll(cls, context):
    return context.mode

  def draw(self, context):
    scene = context.scene
    screen = context.screen
    crg = scene.copyrefgeometryProps
    php = scene.preparehairProps
    layout = self.layout

    box = layout.box()
    col = box.column(align=True)
    col.alignment ='EXPAND'
    col.operator("object.tidy_rename",text="Tidy Rename", icon='OBJECT_DATA')
    col.operator("object.clear_mesh",text="Clear Mesh", icon='OBJECT_DATA')
    
    if context.mode in {'POSE','EDIT_ARMATURE'}:
      box = layout.box()
      col.alignment ='EXPAND'
      column = box.column(align = True)
      column.label(text="Bone Layers")
      row = column.row(align=True)
      row.alignment = 'EXPAND'
      row.prop(context.active_object.data, "layers", toggle=True, text='')
      row = column.row(align=True)

    #See bottom for registration of properties
    box = layout.box()
    row = box.row(align=True)
    row.alignment = 'EXPAND'
    row.operator("object.copy_vert_loc_from_ref", text="Copy Reference Geometry", icon='MESH_DATA')
    row.prop(screen, "crg_expanded",
        icon = "TRIA_DOWN" if screen.crg_expanded else "TRIA_RIGHT",
        icon_only = True, emboss = True
        )
    if screen.crg_expanded:
      col = box.column(align=True)
      col.prop(crg, "p_change", text='Percent Change')
      col.prop(crg, "selected_verts", text='Use Only Selected')
      col.prop(crg, "create_dup", text='Create Duplicate')
      col.prop(crg, "copy_material", text='Copy Material')
      col.prop(crg, "create_shape_key", text='Shape Key')
      col.prop(crg, "shrinkwrap", text='Shrinkwrap')

    #See bottom for registration of properties
    box = layout.box()
    row = box.row(align=True)
    row.prop(screen, "uet_expanded", text="UE4 Export Tools", icon='FILE')
    row.prop(screen, "uet_expanded",
        icon = "TRIA_DOWN" if screen.uet_expanded else "TRIA_RIGHT",
        icon_only = True, emboss = True
        )
    if screen.uet_expanded:
      col = box.column(align=True)
      col.alignment = 'EXPAND'
      col.operator("object.export_sm_to_ue4", text="Export Skeletal Mesh", icon='GROUP')
      col.operator("object.bake_deform_animations", text="Export Animation", icon='POSE_DATA')
      col.operator("object.export_obj_quick", text="Export OBJ", icon='GROUP')
      col.operator("object.import_obj_quick", text="Import OBJ", icon='GROUP')

    #See bottom for registration of properties
    box = layout.box()
    col = box.column(align=True)
    row = col.row(align=True)
    hair = row.operator("object.prep_hair_object", text="Prepare Hair", icon='MESH_DATA')
    row.prop(screen, "ht_expanded",
        icon = "TRIA_DOWN" if screen.ht_expanded else "TRIA_RIGHT",
        icon_only = True, emboss = True
        )
    col.operator("object.prep_hair_movement", text="Prepare Hair Movement", icon='POSE_DATA')
    if screen.ht_expanded:
      col.alignment = 'EXPAND'
      col.prop(php, "hair_material_prefix",text='')
      col.prop(php, "hair_export_object",text='')
      hair.hair_material_prefix = php.hair_material_prefix
      hair.hair_export_object = php.hair_export_object

    # #See bottom for registration of properties
    if context.scene.render.engine == 'CYCLES':
      scene = context.scene
      cscene = scene.cycles
      cbk = scene.render.bake
      box = layout.box()
      col = box.column(align=True)
      row = col.row(align=True)
      row.operator("object.sculpt_bake_prep", text="Bake Prep", icon='OBJECT_DATA')
      row.operator("object.sculpt_export_prep", text="Export Prep", icon='OBJECT_DATA')
      row = col.row(align=True)
      row.operator("object.quick_bake", icon='RENDER_STILL', text='Bake')#.type = cscene.bake_type
      row = col.row(align=True)
      row.prop(cscene, "bake_type", text="")
      row.prop(screen, "bt_expanded",
          icon = "TRIA_DOWN" if screen.bt_expanded else "TRIA_RIGHT",
          icon_only = True, emboss = True
          )
        
      if screen.bt_expanded:
        col = box.column(align=True)

        if cscene.bake_type == 'NORMAL':
            col.prop(cbk, "normal_space", text="")

            row = col.row(align=True)
            row.prop(cbk, "normal_r", text="")
            row.prop(cbk, "normal_g", text="")
            row.prop(cbk, "normal_b", text="")
        
        elif cscene.bake_type == 'AO':
          None
        
        elif cscene.bake_type == 'EMIT':
          None

        elif cscene.bake_type == 'COMBINED':
            row = col.row(align=True)
            row.prop(cbk, "use_pass_direct", toggle=True)
            row.prop(cbk, "use_pass_indirect", toggle=True)

            split = col.split()
            split.active = cbk.use_pass_direct or cbk.use_pass_indirect

            col.prop(cbk, "use_pass_diffuse")
            col.prop(cbk, "use_pass_glossy")
            col.prop(cbk, "use_pass_transmission")

            col.prop(cbk, "use_pass_subsurface")
            col.prop(cbk, "use_pass_ambient_occlusion")
            col.prop(cbk, "use_pass_emit")

        elif cscene.bake_type in {'DIFFUSE', 'GLOSSY', 'TRANSMISSION', 'SUBSURFACE'}:
            row = col.row(align=True)
            row.prop(cbk, "use_pass_direct", toggle=True)
            row.prop(cbk, "use_pass_indirect", toggle=True)
            row.prop(cbk, "use_pass_color", toggle=True)

      col.prop(cbk, "margin")
      col.prop(cbk, "use_clear")

      col.prop(cbk, "use_selected_to_active")
      sub = col.column()
      sub.active = cbk.use_selected_to_active
      sub.prop(cbk, "use_cage", text="Cage")
      if cbk.use_cage:
          sub.prop(cbk, "cage_extrusion", text="Extrusion")
          sub.prop_search(cbk, "cage_object", scene, "objects", text="")
      else:
          sub.prop(cbk, "cage_extrusion", text="Ray Distance")

    # box = layout.box()
    # col = box.column(align=True)
    # col.alignment = 'EXPAND'
    # col.operator("object.flatten_to_uv", text="Flatten Mesh to UV", icon='NONE')

import sys,inspect
classes = (cls[1] for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass))
addon_keymaps = []
# Register the operator
def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)
  #Register Properties
  bpy.types.Scene.copyrefgeometryProps = bpy.props.PointerProperty(type = copy_ref_geometry.crmProps)
  bpy.types.Scene.preparehairProps = bpy.props.PointerProperty(type = mesh_hair_tools.phProps)
  bpy.types.Screen.uet_expanded= bpy.props.BoolProperty(default=False)
  bpy.types.Screen.crg_expanded= bpy.props.BoolProperty(default=False)
  bpy.types.Screen.ht_expanded= bpy.props.BoolProperty(default=False)
  bpy.types.Screen.bt_expanded= bpy.props.BoolProperty(default=True)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)

  # wm = bpy.context.window_manager
  # kc = wm.keyconfigs.addon
  
  # if kc:
  #   #Map Object
  #   km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')

  #   kmi = km.keymap_items.new('object.copy_vert_loc_from_ref', 'E', 'PRESS', alt=True)

  #   addon_keymaps.append([km,kmi])

  #   # Map Mesh
  #   km = kc.keymaps.new('Mesh', space_type='EMPTY', region_type='WINDOW', modal=False)

  #   kmi = km.keymap_items.new('mesh.symmetry_snap', 'X', 'PRESS', alt=True)
  #   kmi = km.keymap_items.new('mesh.remove_doubles', 'D', 'PRESS', ctrl=True)
  #   kmi = km.keymap_items.new('mesh.edge_rotate', 'E', 'PRESS', ctrl=True, shift=True)
  #   kmi = km.keymap_items.new('wm.context_set_value', 'ONE', 'PRESS')
  #   kmi.properties.data_path = 'tool_settings.mesh_select_mode'
  #   kmi.properties.value = 'True,False,False'
  #   kmi = km.keymap_items.new('wm.context_set_value', 'TWO', 'PRESS')
  #   kmi.properties.data_path = 'tool_settings.mesh_select_mode'
  #   kmi.properties.value = 'False,True,False'
  #   kmi = km.keymap_items.new('wm.context_set_value', 'THREE', 'PRESS')
  #   kmi.properties.data_path = 'tool_settings.mesh_select_mode'
  #   kmi.properties.value = 'False,False,True'
  #   kmi = km.keymap_items.new('wm.context_toggle', 'N', 'PRESS', alt=True)
  #   kmi.properties.data_path = 'space_data.use_occlude_geometry'

  #   addon_keymaps.append([km,kmi])

  #   # Map 3D View
  #   km = kc.keymaps.new('3D View Generic', space_type='VIEW_3D', region_type='WINDOW', modal=False)

  #   kmi = km.keymap_items.new('wm.context_toggle_enum', 'T', 'PRESS', shift=True)
  #   kmi.properties.data_path = 'user_preferences.inputs.view_rotate_method'
  #   kmi.properties.value_1 = 'TURNTABLE'
  #   kmi.properties.value_2 = 'TRACKBALL'
  #   kmi = km.keymap_items.new('object.bake_image', 'F12', 'PRESS', alt=True)
  #   kmi = km.keymap_items.new('wm.context_toggle', 'X', 'PRESS', shift=True, alt=True)
  #   kmi.properties.data_path = 'object.show_x_ray'
  #   kmi = km.keymap_items.new('wm.context_toggle', 'W', 'PRESS', shift=True, alt=True)
  #   kmi.properties.data_path = 'object.show_wire'
  #   kmi = km.keymap_items.new('wm.context_toggle', 'R', 'PRESS', shift=True, alt=True)
  #   kmi.properties.data_path = 'space_data.show_only_render'

  #   addon_keymaps.append([km,kmi])

  #   # Map Window
  #   km = kc.keymaps.new('Window', space_type='EMPTY', region_type='WINDOW', modal=False)

  #   kmi = km.keymap_items.new('wm.quick_save', 'W', 'PRESS', ctrl=True)

  #   addon_keymaps.append([km,kmi])

  #   # Map UV Editor
  #   km = kc.keymaps.new('UV Editor', space_type='EMPTY', region_type='WINDOW', modal=False)

  #   kmi = km.keymap_items.new('wm.context_set_enum', 'PERIOD', 'PRESS')
  #   kmi.properties.data_path = 'space_data.pivot_point'
  #   kmi.properties.value = 'CURSOR'
  #   kmi = km.keymap_items.new('wm.context_set_enum', 'COMMA', 'PRESS')
  #   kmi.properties.data_path = 'space_data.pivot_point'
  #   kmi.properties.value = 'CENTER'
  #   kmi = km.keymap_items.new('uv.export_layout', 'E', 'PRESS', ctrl=True)
  #   kmi.properties.export_all = True
  #   kmi.properties.filepath = '//textures'
  #   kmi = km.keymap_items.new('uv.align', 'W', 'PRESS', shift=True)
  #   kmi.properties.axis = 'ALIGN_AUTO'

  #   addon_keymaps.append([km,kmi])

  #   # Map Sculpt
  #   km = kc.keymaps.new('Sculpt', space_type='EMPTY', region_type='WINDOW', modal=False)
  #   kmi = km.keymap_items.new('wm.context_toggle', 'X', 'PRESS', alt=True)
  #   kmi.properties.data_path = 'tool_settings.sculpt.use_symmetry_x'
  #   kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
  #   kmi.properties.name = "paint.pie_brush"

  #   addon_keymaps.append([km,kmi])

  #   #Image Paint
  #   km = kc.keymaps.new('Image Paint', space_type='EMPTY', region_type='WINDOW', modal=False)
  #   kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS')
  #   kmi.properties.name = "paint.pie_brush"

  #   addon_keymaps.append([km,kmi])


  # del bpy.types.Screen.uet_expanded
  # del bpy.types.Screen.grg_expanded
  # del bpy.types.Screen.ht_expanded
  # del bpy.types.WindowManager.copyrefgeometryProps

if __name__ == "__main__":
  register()

