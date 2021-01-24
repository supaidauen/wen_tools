import bpy

class OBJECT_OT_Flatten_to_UV(bpy.types.Operator):
  '''Flatten to UV and back'''

  bl_idname = "object.flatten_to_uv"
  bl_label = "Flatten to UV and back"
  bl_options = {'REGISTER', 'UNDO'}

  @classmethod
  def poll(self, context):
    obj = context.active_object
    return (obj and obj.type == 'MESH' and context.mode == 'OBJECT')

  def execute(self, context):
    ob = bpy.context.active_object
    flatten_to_uv_co(ob)
    return {'FINISHED'}

def flatten_to_uv_co(ob):
  c = ob
  d = c.copy()
  d.data = c.data.copy()
  bpy.context.scene.objects.link(d)
  bpy.context.scene.objects.active = d
  #bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
  print("Duplicated the object")

  me = d.data
  uv_layer = me.uv_layers.active.data

  bpy.ops.object.shape_key_add(from_mix=True)
  print("Added Base shapekey")

  for poly in me.polygons:
    for loop_index in poly.loop_indices:
      i = me.loops[loop_index].vertex_index
      co = uv_layer[loop_index].uv
      me.vertices[i].co[0] = co[0] / bpy.context.scene.unit_settings.scale_length  ## To resize result of UV mesh,
      me.vertices[i].co[1] = co[1] / bpy.context.scene.unit_settings.scale_length  ## change the multiplied ammount
      me.vertices[i].co[2] = 0
  print("Flattened Based on UV")

  bpy.ops.object.shape_key_add(from_mix=False)
  print("Added Morphed shapekey")


def register():
  return
def unregister():
  return
