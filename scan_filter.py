import bpy

bl_info = {
    "name": "Scan Filter",
    "description": "Tool for filtering 3D scanned geometry from floor and artifacts.",
    "author": "Roman Chumak",
    "version": (0, 0, 1, 3),
    "blender": (2, 80, 0),
    "location": "View3D",
    "category": "Object"}



class P4ScanFilterProperties(bpy.types.PropertyGroup):
    lim_loc_z = bpy.props.FloatProperty(default = 0.3, min = 0, max = 1, description = "The ratio of floor height to the total height of the bounding box.\nDefault =  0.3")
    lim_nor_z = bpy.props.FloatProperty(default = 0.2, min = 0, max = 1, description = "Permissible angular variation between floor polygons and XY plane.\nDefault =  0.2")
    lim_poly = bpy.props.FloatProperty(default = 0.05, min = 0, max = 1, description = "Percentage of polygons per disconnected islands to be deleted.\nDefault =  0.05")
    lim_dist = bpy.props.FloatProperty(default = 0.2, min = 0, max = 1, description = "Area from center on XY plane to preserve geometry.\nDefault =  0.2")



class P4ScanFilter(bpy.types.Operator):
    """Filter 3D scanned geometry from floor and artefacts."""
    bl_idname = 'p4scanfilter.exec'
    bl_label = 'Filter'
    bl_options={'INTERNAL'}
    
    def execute(self, context):
        print("*********")
        print(P4ScanFilterProperties.lim_loc_z[0])
        
        limLocZ = context.scene.p4_scan_filter.lim_loc_z
        limNorZ = context.scene.p4_scan_filter.lim_nor_z
        limPoly = context.scene.p4_scan_filter.lim_poly 
        limDist = context.scene.p4_scan_filter.lim_dist 
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        obj = bpy.context.active_object
        mesh = obj.data
        vertsTotal = len(obj.data.vertices)

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        locX = obj.location[0]
        locY = obj.location[1]

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()

        dim = obj.dimensions
        lowLim = (limLocZ - 1) * dim[2] / 2
        distMax = (dim[0]/2)**2 + (dim[1]/2)**2


        for poly in mesh.polygons:
            if poly.center[2] <= lowLim and abs(poly.normal[2]) >= 1 - limNorZ:
                poly.select = True
                

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.editmode_toggle()

        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')


        for obj in bpy.context.selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            dist = ((obj.location[0] - locX)**2 + (obj.location[1] - locY)**2) / distMax
            verts = len(obj.data.vertices)
              
            if verts <= vertsTotal * limPoly:
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete(use_global=False)

            elif  dist > limDist:
                bpy.data.objects[obj.name].select_set(True)
                bpy.ops.object.delete(use_global=False)
        
        return {'FINISHED'}


            
class OBJECT_PT_P4ScanFilterPanel(bpy.types.Panel):
    bl_label = "Scan Filter"
    bl_idname = "Scan_Filter"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        col = layout.column()
        col.prop(context.scene.p4_scan_filter, 'lim_loc_z', text="Floor Height Limit")
        col.prop(context.scene.p4_scan_filter, 'lim_nor_z', text="Floor Normal Limit")
        col.prop(context.scene.p4_scan_filter, 'lim_poly', text="Artifacts")
        col.prop(context.scene.p4_scan_filter, 'lim_dist', text="Area of interest")
        
        col.operator("p4scanfilter.exec", icon='MOD_MESHDEFORM')
        

        
def register():
    bpy.utils.register_class(P4ScanFilterProperties)
    bpy.types.Scene.p4_scan_filter = bpy.props.PointerProperty(type=P4ScanFilterProperties)
    bpy.utils.register_class(P4ScanFilter)
    bpy.utils.register_class(OBJECT_PT_P4ScanFilterPanel)
    
def unregister():
    del bpy.types.Scene.p4_scan_filter
    bpy.utils.unregister_class(P4ScanFilterProperties)
    bpy.utils.unregister_class(P4ScanFilter)
    bpy.utils.unregister_class(OBJECT_PT_P4ScanFilterPanel)
    
if __name__ == "__main__":
    register()