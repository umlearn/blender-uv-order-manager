import bpy
from bpy.types import Operator

bl_info = {
	"name": "UV Order ",
	"author": "UMLEARN", 
	"version": (1, 0),
	"blender": (3, 0, 0),
	"doc_url": "https://github.com/umlearn/blender-uv-order-manager",	
	"location": "Properties > Object Data > UV Maps",
	"description": "UV layer organization tools",
	"category": "UV"
}

def get_uv_data():
	return bpy.context.active_object.data.uv_layers

def activate_layer(layer_name):
	uv_data = get_uv_data()
	for layer in uv_data:
		if layer.name == layer_name:
			uv_data.active = layer
			return

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

def draw_manager_ui(self, context):
	layout = self.layout
	# box = layout.box()
	row = layout.row(align=True)
	row.operator("uv.move_to_start", text="", icon='TRIA_UP_BAR')
	row.operator("uv.move_up", text="", icon='TRIA_UP')
	row.operator("uv.move_down", text="", icon='TRIA_DOWN')
	row.operator("uv.move_to_end", text="", icon='TRIA_DOWN_BAR')

classes = (
	MoveLayerToTop,
	MoveLayerUp,
	MoveLayerDown,
	MoveLayerToBottom
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.DATA_PT_uv_texture.append(draw_manager_ui)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	bpy.types.DATA_PT_uv_texture.remove(draw_manager_ui)

if __name__ == "__main__":
	register()