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
  bl_category = "Wen Tools"


  @classmethod
  def poll(cls, context):
    return context.mode

  def draw(self, context):
    scene = context.scene
    screen = context.screen
    crg = scene.copyrefgeometryProps
    php = scene.preparehairProps
    layout = self.layout
    amum = context.scene.applymultiusermodifierprops
    box = layout.box()
    col = box.column(align=True)
    col.alignment ='EXPAND'
    col.operator("object.tidy_rename", text="Tidy Rename", icon='OBJECT_DATA')
    col.operator("object.clear_mesh", text="Clear Mesh", icon='OBJECT_DATA')
    col.operator("object.apply_multi_user_modifier", text="Apply Multi User Modifier", icon='OBJECT_DATA')
    row = col.row()
    row.prop(amum, "keep_modifier", text="Keep Modifier")
    row = col.row()
    row.prop(amum, "selected_modifier", text="", emboss=True)
    
    if context.mode in {'POSE','EDIT_ARMATURE'}:
      box = layout.box()
      col.alignment ='EXPAND'
      column = box.column(align = True)
      column.label(text="Bone Layers")
      row = column.row(align=True)
      row.alignment = 'EXPAND'
      row.prop(context.active_object.data, "layers", toggle=True, text='')
      row = column.row(align=True)

    # See bottom for registration of properties
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

    # See bottom for registration of properties
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
      col.operator("object.bake_deform_animations", text="Export Animation", icon='ARMATURE_DATA')
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
    if screen.ht_expanded:
      col.alignment = 'EXPAND'
      col.prop(php, "hair_material_prefix",text='')
      col.prop(php, "hair_export_object",text='')
      hair.hair_material_prefix = php.hair_material_prefix
      hair.hair_export_object = php.hair_export_object
    col.operator("object.prep_hair_movement", text="Prepare Hair Movement", icon='ARMATURE_DATA')

    # See bottom for registration of properties
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

classes = (
VIEW_3D_PT_WenToolsPanel,
)


# Register the operator
def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)
  # Register Properties
  bpy.types.Scene.copyrefgeometryProps = bpy.props.PointerProperty(type=copy_ref_geometry.crmProps)
  bpy.types.Scene.preparehairProps = bpy.props.PointerProperty(type=mesh_hair_tools.phProps)
  bpy.types.Scene.applymultiusermodifierprops = bpy.props.PointerProperty(type=basic_ops.amumProps)
  bpy.types.Screen.uet_expanded = bpy.props.BoolProperty(default=False)
  bpy.types.Screen.crg_expanded = bpy.props.BoolProperty(default=False)
  bpy.types.Screen.ht_expanded = bpy.props.BoolProperty(default=False)
  bpy.types.Screen.bt_expanded = bpy.props.BoolProperty(default=True)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
  del bpy.types.Scene.copyrefgeometryProps
  del bpy.types.Scene.preparehairProps
  del bpy.types.Scene.applymultiusermodifierprops
  del bpy.types.Scene.dyn_list
  del bpy.types.Screen.uet_expanded
  del bpy.types.Screen.crg_expanded
  del bpy.types.Screen.ht_expanded
  del bpy.types.Screen.bt_expanded

if __name__ == "__main__":
  register()
