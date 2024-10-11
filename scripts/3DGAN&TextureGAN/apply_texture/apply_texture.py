import bpy
import os
import sys
import random
def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    import argparse
    parser = argparse.ArgumentParser(
        description='Apply textures to multiple OBJ files and generate corresponding MTL files.')
    parser.add_argument('--obj_folder', type=str, required=True, help='Path to the folder containing OBJ files.')
    parser.add_argument('--texture_folder', type=str, required=True,
                        help='Path to the folder containing PNG texture files.')
    parser.add_argument('--output_folder', type=str, required=True, help='Path to the output folder.')
    args = parser.parse_args(argv)
    return args

def apply_texture_and_export(obj_path, texture_path, output_folder):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=obj_path)
    obj = bpy.context.selected_objects[0]

    # 进入编辑模式进行UV编辑
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    for oWindow in bpy.context.window_manager.windows:
        oScreen = oWindow.screen
        for oArea in oScreen.areas:
            if oArea.type == 'VIEW_3D':
                for oRegion in oArea.regions:
                    if oRegion.type == 'WINDOW':
                        context_override = bpy.context.copy()  # EDITED
                        override = {
                            'window': oWindow,
                            'screen': oScreen,
                            'area': oArea,
                            'region': oRegion,
                            'scene': bpy.context.scene,
                            'edit_object': bpy.context.edit_object,
                            'active_object': bpy.context.active_object,
                            'selected_objects': bpy.context.selected_objects
                        }
                        for k, v in override.items():  # EDITED
                            context_override[k] = v
                        with bpy.context.temp_override(**context_override):  # EDITED
                            bpy.ops.uv.project_from_view(camera_bounds=True, correct_aspect=False,
                                                         scale_to_bounds=True)
    # 返回对象模式
    bpy.ops.object.mode_set(mode='OBJECT')

    # 创建材质并应用纹理
    mat = bpy.data.materials.new(name="Material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(texture_path)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    base_name = os.path.splitext(os.path.basename(obj_path))[0]
    obj_output_folder = os.path.join(output_folder, base_name)
    os.makedirs(obj_output_folder, exist_ok=True)

    output_obj_path = os.path.join(obj_output_folder, "model.obj")
    bpy.ops.wm.obj_export(filepath=output_obj_path)
    print(f"Exported {output_obj_path}")

if __name__ == "__main__":
    args = parse_args()

    obj_files = sorted([f for f in os.listdir(args.obj_folder) if f.endswith('.obj')])
    texture_files = sorted([f for f in os.listdir(args.texture_folder) if f.endswith('.jpg')])

    if len(obj_files) != len(texture_files):
        raise ValueError("The number of OBJ files and texture files must be the same.")

    combined_list = list(zip(obj_files, texture_files))
    random.shuffle(combined_list)
    obj_files, texture_files = zip(*combined_list)

    for obj_file, texture_file in zip(obj_files, texture_files):
        obj_path = os.path.join(args.obj_folder, obj_file)
        texture_path = os.path.join(args.texture_folder, texture_file)
        apply_texture_and_export(obj_path, texture_path, args.output_folder)
