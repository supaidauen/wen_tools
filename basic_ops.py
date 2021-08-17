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
from bpy.props import BoolProperty,EnumProperty,FloatProperty

class OBJECT_OT_Display_Wireframe_Toggle(bpy.types.Operator):
  '''Display Wireframe'''
  bl_idname = "object.display_as_wireframe"
  bl_label = "Display as Wireframe"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    obj = context.active_object
    if hasattr(obj, 'display_type'):
      return (obj)
  def execute(self, context):
    ob = context.active_object
    if not 'display_type' in ob:
        ob['display_type'] = ob.display_type
    if ob['display_type'] == 'WIRE':
      ob.pop('display_type', None)
      return {'FINISHED'}
    elif ob.display_type == ob['display_type']:
        ob.display_type = 'WIRE'
    else:
        ob.display_type = ob['display_type']
        ob.pop('display_type', None)
    return {'FINISHED'}

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
      baker.data =  ob.to_mesh(preserve_all_data_layers=True, depsgraph='PREVIEW')
      baker.animation_data_clear()
      baker.modifiers.clear()
      scn.objects.link(baker)
    else:
      baker = data.objects['baker']
      baker.data = ob.to_mesh(preserve_all_data_layers=True, depsgraph='PREVIEW')

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
    
    # for i in range(len(scn.layers)):
    #   if i in [5]:
    #     baker.layers[i] = True
    #     cage.layers[i] = True
    #   else:
    #     baker.layers[i] = False
    #     cage.layers[i] = False

    # baker.layers[scn.active_layer] = False
    # cage.layers[scn.active_layer] = False

    for v in cage.data.vertices:
      v.co += v.normal * 0.4

    cagewrap = cage.modifiers.new("Shrinkwrap",'Shrinkwrap'.upper())
    cagewrap.target = data.objects[cageref]
    cagewrap.use_keep_above_surface = True
    cage.data = cage.to_mesh(preserve_all_data_layers=True, depsgraph='PREVIEW')
    cage.data.name = 'cage'
    cage.modifiers.remove(cagewrap)

    cage.select_set(False)
    ob.select_set(False)
    sculpt.select_set(True)
    baker.select_set(True)
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
        nodes['T_N'].select_set(True)
        nodes.active = nodes['T_N']

      elif cscene.bake_type == 'AO':
        scene.render.bake.use_selected_to_active = True
        nodes['T_AO'].select_set(True)
        nodes.active = nodes['T_AO']
        
      elif cscene.bake_type == 'EMIT':
        scene.render.bake.use_selected_to_active = False
        nodes['T_D'].select_set(True)
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

def mods_cb(self, context):
  ob = context.active_object
  modifiers = ob.modifiers
  mods = ((mod.name, mod.name, "Apply "+mod.type) for mod in modifiers)
  return mods

def update_mods_cb(self, context):
  amum = context.scene.amumProps
  return amum

class AMUM_Props(bpy.types.PropertyGroup):
  keep_modifier: BoolProperty(
    description="Keep copy of Modifier",
    default=True
  )
  selected_modifier: EnumProperty(
    items=mods_cb,
    update=update_mods_cb,
    description="Modifiers",
    name="Modifiers"
  )

class OBJECT_OT_Apply_Multi_User_Modifier(bpy.types.Operator):
  '''Apply Modifier to Mutli User Data'''

  bl_idname = "object.apply_multi_user_modifier"
  bl_label = "Apply Multi User Modifier"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(cls, context):
    return (context.active_object is not None and 
            context.active_object.type == 'MESH')

  def execute(self, context):
    amum = context.scene.amumProps
    C = bpy.context
    D = bpy.data
    ob = C.active_object
    obs_temp = []
    temp = D.objects.data.meshes.new(name='temp')
    keep_modifier = amum.keep_modifier
    selected_modifier = amum.selected_modifier
    name = ob.modifiers[selected_modifier].name
    for obs in D.objects:
      if obs.data == ob.data and obs != ob:
        obs_temp.append(obs)
        obs.data = temp
    if keep_modifier:
      old_modifiers = [modifier.name for modifier in ob.modifiers]
      bpy.ops.object.modifier_copy(modifier=selected_modifier)
      for modifier in ob.modifiers:
        if modifier.name not in old_modifiers:
          copy = modifier
      bpy.ops.object.modifier_apply(modifier=selected_modifier)
      copy.name = name
    else:
      bpy.ops.object.modifier_apply(modifier=selected_modifier)
    for obs in obs_temp:
        obs.data = ob.data
    D.meshes.remove(temp)
    return {'FINISHED'}

class OBJECT_OT_Empty_At_Bone_Tail(bpy.types.Operator):
  '''Set Empty at Bone tail for Active Armature'''

  bl_idname = "object.put_empty_at_bone_tail"
  bl_label = "Empty at Bone Tail"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(cls, context):
    return (context.active_object is not None and 
            context.active_object.type == 'ARMATURE')

  def execute(self,context):
    def empty_at_bone_tail():
      ob = context.active_object
      E = bpy.data.objects.new("E_"+ob.name,None)
      bpy.context.scene.collection.objects.link(E)
      E.location = ob.location
      E.empty_display_size = 0.01
      E.show_in_front = True
      parent = E
      for b in ob.data.bones:
        E = bpy.data.objects.new("E_"+b.name,None)
        bpy.context.scene.collection.objects.link(E)
        E.location = b.tail_local
        E.empty_display_size = 0.01
        E.parent = parent
        E.show_in_front = True
    empty_at_bone_tail()
    return {'FINISHED'}

class OBJECT_OT_Origin_to_world_center(bpy.types.Operator):
  '''Sets selected objects origins to world center'''

  bl_idname = "object.set_origin_to_world_center"
  bl_label = "Set Object Origin to world center"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(cls, context):
    return (context.active_object is not None)

  def execute(self,context):
    def get_cursor_location():
      location = bpy.context.scene.cursor.location
      return (location.x,location.y,location.z)
    from mathutils import Vector
    original_location = get_cursor_location()
    bpy.context.scene.cursor.location = Vector((0.0,0.0,0.0))
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.context.scene.cursor.location = Vector(original_location)
    return {'FINISHED'}

class OBJECT_OT_Set_Paint_Weight(bpy.types.Operator):
  '''Sets weight in Vertex Weight Paint Mode'''

  bl_idname = "object.set_paint_weight"
  bl_label = "Set weight amount"
  bl_options = {'REGISTER', 'UNDO'}

  weight_amt: FloatProperty(
    name="Weight Amount",
    description="Weight Amount",
    default=0.0
  )

  @classmethod
  def poll(cls, context):
    return (context.active_object is not None and
            context.active_object.type == 'MESH' and
            context.mode == 'PAINT_WEIGHT')

  def execute(self,context):
    bpy.context.tool_settings.unified_paint_settings.weight = self.weight_amt
    bpy.context.tool_settings.weight_paint.brush.weight = self.weight_amt
    return {'FINISHED'}

class OBJECT_OT_Merge_to_Mesh(bpy.types.Operator):
  '''Merges Selected Objects to a single mesh'''

  bl_idname = "object.merge_to_mesh"
  bl_label = "Merge to Mesh"
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self,context):
    C = bpy.context
    D = bpy.data
    name = C.active_object.name
    scn = C.scene
    obs = C.selected_objects
    meshes = []
    for ob in obs:
      if hasattr(ob.data, "use_uv_as_generated"):
        ob.data.use_uv_as_generated = True
      depsgraph = context.evaluated_depsgraph_get()
      ob_eval = ob.evaluated_get(depsgraph)
      mesh = D.meshes.new_from_object(ob_eval)
      ob.select_set(False)
      mesh.name = ob.name+"_temp"
      new_object = D.objects.new(ob.name+"_temp", mesh)
      C.scene.collection.objects.link(new_object)
      # C.view_layer.active_layer_collection.collection.objects.link(new_object)
      new_object.select_set(True)
      meshes.append(new_object)
      try:
        new_object.data.uv_layers[0].name = "UVMap"
      except IndexError:
        self.report({'ERROR'}, "All objects must have at least one UV...\n(For curves check 'Use UV for mapping')")
        for mesh in meshes:
          D.objects.remove(mesh)
        return {'CANCELLED'}
      finally:
        "moving along"
    ctx = {}
    active_object = meshes[0]
    ctx['object'] = ctx['active_object'] = active_object
    ctx['selected_objects'] = ctx['selectable_editable_objects'] = meshes
    bpy.ops.object.join(ctx)
    active_object.name = name + "_new"
    bpy.context.view_layer.objects.active = active_object
    C.view_layer.objects.update()

    return {'FINISHED'}

class OBJECT_OT_Fix_Symmetry(bpy.types.Operator):
  '''Fixes Symmetry of a mesh by aligning X and weightgroups'''

  bl_idname = "object.fix_symmetry"
  bl_label = "Fix Symmetry"
  bl_options = {'REGISTER', 'UNDO'}

  def execute(self,context):
    C = bpy.context
    D = bpy.data

    mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    ob = C.active_object
    for v in ob.data.vertices:
        old_orient = "_r" if v.co.x > 0 else "_l" 
        new_orient = "_l" if v.co.x > 0 else "_r" 
        for g in v.groups:
            name = ob.vertex_groups[g.group].name
            vgroup = ob.vertex_groups[g.group]
            if old_orient in name:
                new_group = name.replace(old_orient,new_orient)
                new_group_index = ob.vertex_groups[new_group].index
                new_vgroup = ob.vertex_groups[new_group_index]
                new_group_weight = g.weight
                vgroup.remove([v.index])
                new_vgroup.add([v.index],new_group_weight,'REPLACE')
                
    for v in ob.data.vertices:
        if v.select:
            if ob.data.shape_keys:
                n = ob.active_shape_key.name
                sk = ob.data.shape_keys.key_blocks[n]
                v = sk.data[v.index]
            v.co.x = 0
    print(mode)
    bpy.ops.object.mode_set(mode=mode)
    C.view_layer.update()
    
    return {'FINISHED'}

classes = (
AMUM_Props,
OBJECT_OT_Display_Wireframe_Toggle,
OBJECT_OT_Clear_Mesh,
OBJECT_OT_Image_Save_Options,
OBJECT_OT_Pose_Rest_Toggle,
OBJECT_OT_Quick_Bake,
OBJECT_OT_Sculpt_Bake_Prep,
OBJECT_OT_Sculpt_Export_Prep,
OBJECT_OT_Tidy_Rename,
OBJECT_OT_Apply_Multi_User_Modifier,
OBJECT_OT_Empty_At_Bone_Tail,
OBJECT_OT_Origin_to_world_center,
OBJECT_OT_Set_Paint_Weight,
OBJECT_OT_Merge_to_Mesh,
OBJECT_OT_Fix_Symmetry,
)

def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
