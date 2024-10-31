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

import bpy
from . import uv_order

def draw_manager_ui(self, context):
	layout = self.layout
	row = layout.row(align=True)
	row.operator("uv.move_to_start", text="", icon='TRIA_UP_BAR')
	row.operator("uv.move_up", text="", icon='TRIA_UP')
	row.operator("uv.move_down", text="", icon='TRIA_DOWN')
	row.operator("uv.move_to_end", text="", icon='TRIA_DOWN_BAR')
	
def register():
	for cls in uv_order.classes:
		bpy.utils.register_class(cls)
	bpy.types.DATA_PT_uv_texture.append(draw_manager_ui)

def unregister():
	for cls in reversed(uv_order.classes):
		bpy.utils.unregister_class(cls)
	bpy.types.DATA_PT_uv_texture.remove(draw_manager_ui)

if __name__ == "__main__":
	register()