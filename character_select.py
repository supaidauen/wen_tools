import bpy
from bpy.props import EnumProperty

def characters_text():
  data = bpy.data
  try:
    characters_text = data.texts['characters'].as_module()
    # print(characters_text.characters)
    characters = characters_text.characters
  except:
    characters = {"__None__":("","","")}
  return characters

def characters(self, context):
  characters = ((character,character, "") for character in characters_text())
  return characters

def characters_populate(self, context):
   return

class CS_Props(bpy.types.PropertyGroup):
  character: EnumProperty(
    items=characters,
    update=characters_populate,
    description="Characters",
    name="Characters"
  )

class OBJECT_OT_Character_Select(bpy.types.Operator):
  '''Character Select'''

  bl_idname = "object.character_select"
  bl_label = "Character Select"
  bl_options = {'REGISTER', 'UNDO'}

  characters: EnumProperty(
    items=characters,
    update=characters_populate,
    description="Characters",
    name="Characters"
  )

  def execute(self, context):
    data = bpy.data
    character_name = self.characters
    context.scene.csProps.character = character_name
    character = characters_text()[character_name]
    name,eye_color,skin_color,hair_root,hair_shaft,hair_texture=character['name'], \
    character['eye_color'], \
    character['skin_color'], \
    character['hair_root'], \
    character['hair_shaft'], \
    character['hair_texture']

    obs = [ob for ob in data.objects if "base." in ob.name]
    hair_cols = [collection for collection in bpy.data.collections if "hairmesh" in collection.name]

    for ob in obs:
      try:
        keys = ob.data.shape_keys.key_blocks.keys()
        idx = keys.index(name)
        ob.active_shape_key_index = idx
      except:
        None
      if 'eyes' in ob.name:
        ob.material_slots[0].material.node_tree.nodes['eyecolor'].image = data.images[eye_color]
      if 'skin_color' in ob.keys():
        ob['skin_color'] = skin_color
      else:
        continue
    bpy.data.materials['base_hair'].node_tree.nodes['hair_root'].inputs['Color2'].default_value = hair_root
    bpy.data.materials['base_hair'].node_tree.nodes['hair_shaft'].inputs['Color2'].default_value = hair_shaft
    bpy.data.materials['base_hair'].node_tree.nodes['hair_texture'].image = data.images[hair_texture]
    for collection in hair_cols:
      collection.hide_render = True
      collection.hide_select = True
      collection.hide_viewport = True

      if name in collection.name:
        collection.hide_render = False
        collection.hide_select = False
        collection.hide_viewport = False
    
    return {'FINISHED'}

classes = (
  CS_Props,
  OBJECT_OT_Character_Select,
)

def register():
  from bpy.utils import register_class
  for cls in classes:
    register_class(cls)

def unregister():
  from bpy.utils import unregister_class
  for cls in reversed(classes):
    unregister_class(cls)
