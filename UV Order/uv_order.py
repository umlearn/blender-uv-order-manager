import bpy
from bpy.types import Operator

def get_uv_data():
    return bpy.context.active_object.data.uv_layers

def activate_layer(layer_name):
    uv_data = get_uv_data()
    for layer in uv_data:
        if layer.name == layer_name:
            uv_data.active = layer
            break

def reposition_layer(index):
    uv_data = get_uv_data()
    uv_data.active_index = index
    current_name = uv_data.active.name
    
    bpy.ops.mesh.uv_texture_add()
    activate_layer(current_name)
    bpy.ops.mesh.uv_texture_remove()
    
    uv_data.active_index = len(uv_data) - 1
    uv_data.active.name = current_name

class MoveLayerToTop(Operator):
    bl_idname = "uv.move_to_start"
    bl_label = "To Start"
    bl_description = "Move selected UV layer to the beginning"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        uv_data = get_uv_data()
        start_idx = uv_data.active_index
        layer_name = uv_data.active.name
        
        if start_idx == 0:
            return {'FINISHED'}
            
        reposition_layer(start_idx)
        for _ in range(len(uv_data) - 1):
            reposition_layer(0)
        
        activate_layer(layer_name)
        return {'FINISHED'}

class MoveLayerUp(Operator):
    bl_idname = "uv.move_up"
    bl_label = "Layer Up"
    bl_description = "Move selected UV layer up"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        uv_data = get_uv_data()
        if uv_data.active_index == 0:
            return {'FINISHED'}
        
        layer_name = uv_data.active.name
        uv_data.active_index -= 1
        bpy.ops.uv.move_down()
        activate_layer(layer_name)
        return {'FINISHED'}

class MoveLayerDown(Operator):
    bl_idname = "uv.move_down"
    bl_label = "Layer Down"
    bl_description = "Move selected UV layer down"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        uv_data = get_uv_data()
        current_idx = uv_data.active_index
        layer_name = uv_data.active.name
        
        if current_idx == len(uv_data) - 1:
            return {'FINISHED'}
        
        reposition_layer(current_idx + 1)
        reposition_layer(current_idx)
        
        for _ in range(current_idx, len(uv_data) - 2):
            reposition_layer(current_idx)
            
        activate_layer(layer_name)
        return {'FINISHED'}

class MoveLayerToBottom(Operator):
    bl_idname = "uv.move_to_end"
    bl_label = "To End"
    bl_description = "Move selected UV layer to the end"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        uv_data = get_uv_data()
        current_idx = uv_data.active_index
        layer_name = uv_data.active.name
        
        if current_idx == len(uv_data) - 1:
            return {'FINISHED'}

        reposition_layer(current_idx)
        activate_layer(layer_name)
        return {'FINISHED'}

classes = (
    MoveLayerToTop,
    MoveLayerUp,
    MoveLayerDown,
    MoveLayerToBottom
)
