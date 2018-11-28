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

class OBJECT_OT_Clear_Mesh(bpy.types.Operator):
  '''Clear Mesh'''
  
  bl_idname = "object.clear_mesh"
  bl_label = "Clear Mesh"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    obj = context.active_object
    if hasattr(obj, "type"):
      return (obj and obj.type == 'MESH')

  def execute(self, context):
    cont = bpy.context
    data = bpy.data
    ob = cont.active_object
    mats = ob.data.materials
    vgroups = ob.vertex_groups
    clear = ob.data
    name = clear.name
    me = data.meshes.new(name)
    ob.data = me
    for mat in mats:
      ob.data.materials.append(mat)
    for vgroup in vgroups:
      if vgroup.name not in ob.vertex_groups.keys():
        ob.vertex_groups.new(vgroup.name)
    me.name = clear.name
    clear.user_clear()
    data.meshes.remove(clear)
    
    return {'FINISHED'}

class OBJECT_OT_Sculpt_Bake_Prep(bpy.types.Operator):
  '''Prep Sculpted Objects'''
  
  bl_idname = "object.sculpt_bake_prep"
  bl_label = "Prep HiRes"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    ob = context.active_object
    obs = context.selected_objects
    if hasattr(ob, "type") and len(obs) == 1:
      return (ob and ob.type == 'MESH')
  
  def execute(self, context):
    cont = bpy.context
    data = bpy.data
    scn = cont.scene
    ob = cont.active_object
    sculpt = data.objects[ob.name.replace('geo','sculpt')]
    cageref = ob.name.replace('geo','cageref')
    Basis = ob.data.shape_keys.key_blocks.find('Basis')
    Bake = ob.data.shape_keys.key_blocks.find('Bake')

    sculpt.active_shape_key_index = Bake
    ob.active_shape_key_index = Bake
    scn.update()

    if 'baker' not in data.objects:
      baker = ob.copy()
      baker.name = 'baker'
      baker.data =  ob.to_mesh(scn, True, 'PREVIEW')
      baker.animation_data_clear()
      baker.modifiers.clear()
      scn.objects.link(baker)
    else:
      baker = data.objects['baker']
      baker.data = ob.to_mesh(scn, True, 'PREVIEW')

    if 'cage' not in data.objects:
      cage = ob.copy()
      cage.name = 'cage'
      cage.data = baker.data.copy()
      cage.animation_data_clear()
      cage.modifiers.clear()
      scn.objects.link(cage)
    else:
      cage = data.objects['cage']
      cage.data = baker.data.copy()

    baker.data.name = 'baker'
    baker.data.materials.clear()
    baker.data.materials.append(data.materials['baker_material'])
    for face in baker.data.uv_textures.active.data:
      face.image = data.images["i_mask_clothes_skin"]
    cage.data.name = 'cage'
    cage.data.materials.clear()
    cont.scene.objects.active = baker
    
    for i in range(len(scn.layers)):
      if i in [5]:
        baker.layers[i] = True
        cage.layers[i] = True
      else:
        baker.layers[i] = False
        cage.layers[i] = False

    baker.layers[scn.active_layer] = False
    cage.layers[scn.active_layer] = False

    for v in cage.data.vertices:
      v.co += v.normal * 0.4

    cagewrap = cage.modifiers.new("Shrinkwrap",'Shrinkwrap'.upper())
    cagewrap.target = data.objects[cageref]
    cagewrap.use_keep_above_surface = True
    cage.data = cage.to_mesh(scn, True, 'PREVIEW')
    cage.data.name = 'cage'
    cage.modifiers.remove(cagewrap)

    cage.select = False
    ob.select = False
    sculpt.select = True
    baker.select = True
    scn.update()

    scn.update()

    return {'FINISHED'}

class OBJECT_OT_Sculpt_Export_Prep(bpy.types.Operator):
  '''Prep Sculpted Objects'''
  
  bl_idname = "object.sculpt_export_prep"
  bl_label = "Prep Export After Baking"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    ob = context.active_object
    obs = context.selected_objects
    if hasattr(ob, "type") and len(obs) == 1:
      return (ob and ob.type == 'MESH')
  
  def execute(self, context):
    cont = bpy.context
    data = bpy.data
    scn = cont.scene
    ob = cont.active_object
    sculpt = data.objects[ob.name.replace('geo','sculpt')]
    Basis = ob.data.shape_keys.key_blocks.find('Basis')

    sculpt.active_shape_key_index = Basis
    ob.active_shape_key_index = Basis
    scn.update()

    return {'FINISHED'}

class OBJECT_OT_Quick_Bake(bpy.types.Operator):
  '''Quick Bake'''

  bl_idname = "object.quick_bake"
  bl_label = "Quick Bake"
  bl_options = {'REGISTER'}

  @classmethod
  def poll(self, context):
    ob = context.active_object
    obs = context.selected_objects
    if hasattr(ob, "type") and len(obs) <= 2:
      return (ob and ob.type == 'MESH')

  def execute(self, context):
    cont = bpy.context
    ob = cont.active_object
    scene = context.scene
    cscene = scene.cycles
    if 'baker_material' in ob.data.materials:
      nodes = ob.data.materials['baker_material'].node_tree.nodes
      
      if cscene.bake_type == 'NORMAL':
        scene.render.bake.use_selected_to_active = True
        nodes['T_N'].select = True
        nodes.active = nodes['T_N']

      elif cscene.bake_type == 'AO':
        scene.render.bake.use_selected_to_active = True
        nodes['T_AO'].select = True
        nodes.active = nodes['T_AO']
        
      elif cscene.bake_type == 'EMIT':
        scene.render.bake.use_selected_to_active = False
        nodes['T_D'].select = True
        nodes.active = nodes['T_D']

    bpy.ops.object.bake(type=cscene.bake_type)

    return {'FINISHED'}

class OBJECT_OT_Tidy_Rename(bpy.types.Operator):
  '''Rename Tidily'''
  
  bl_idname = "object.tidy_rename"
  bl_label = "Tidy Rename"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self, context):
    cont = bpy.context
    for ob in cont.selected_objects:
      if ob.type == 'MESH':
        ob.data.name = ob.name.replace("obj","mesh")
      elif ob.type == 'ARMATURE':
        ob.data.name = ob.name.replace("obj","arm")
      elif ob.type == 'LAMP':
        ob.data.name = ob.name.replace("obj","lmp")
      elif ob.type == 'CURVE':
        ob.data.name = ob.name.replace("obj","crv")
      else:
        pass
    return {'FINISHED'}

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

class OBJECT_OT_Quick_Save(bpy.types.Operator):
  '''Save Immediately'''

  bl_idname = "wm.quick_save"
  bl_label = "Quick Save"
  bl_options = {'REGISTER', 'UNDO'}
  
  def execute(self, context):
    bpy.ops.wm.save_mainfile(check_existing=False, compress=True,)
    return {'FINISHED'}

class OBJECT_OT_Image_Save_Options(bpy.types.Operator):
    '''Image Save Options'''
    
    bl_idname = "save.image_save_options"
    bl_label = "Image Save Options"
    bl_description = "Better Image Save Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(name="File Path", description="Path where the image will be saved", maxlen=1024, default="")
    filter_folder: bpy.props.BoolProperty(name="Filter folders", description="", default=True, options={'HIDDEN'})
    # imageFileType: bpy.props.EnumProperty(items=[('PNG Save',)])
    
    def execute(self, context):
        self.save_image()
        return {'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    def save_image(self):
        img = bpy.context.space_data.image
        bpy.context.scene.render.image_settings.file_format = 'PNG'

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
