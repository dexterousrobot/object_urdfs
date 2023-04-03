import os
import shutil
from object2urdf import ObjectUrdfBuilder
from cleanup_tools import get_immediate_subdirectories
import argparse
import shapenet
from glob import glob
import point_cloud_utils as pcu
import numpy as np
import trimesh


def as_mesh(scene_or_mesh):
    # Utils function that returns a mesh from a trimesh.Trimesh() or trimesh.scene.Scene()
    if isinstance(scene_or_mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate([
            trimesh.Trimesh(vertices=m.vertices, faces=m.faces)
            for m in scene_or_mesh.geometry.values()])
    else:
        mesh = scene_or_mesh
    return mesh


# Update file
def replace_in_file(filepath, original, replacement):
    """Replace original string with replacement string in file at filepath.
    These can be single strings or list of strings."""
    with open(filepath, "r") as file:
        filedata = file.read()

    original = [original] if not isinstance(original, list) else original
    replacement = [replacement] if not isinstance(replacement, list) else replacement
    assert len(original) == len(replacement)

    for idx in range(len(original)):
        filedata = filedata.replace(original[idx], replacement[idx])

    with open(filepath, "w") as file:
        file.write(filedata)


def main(args):
    # Create new directory to place processed files
    new_folder = os.path.join(os.path.dirname(shapenet.__file__), 'ShapeNetCoreV2urdf')
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Create __init__.py file
    initfile = os.path.join(new_folder, '__init__.py')
    try:
        open(initfile, 'x')
    except FileExistsError:
        pass

    shapenet_folder = os.path.join(os.path.dirname(shapenet.__file__), 'ShapeNetCoreV2')

    subdirs = get_immediate_subdirectories(shapenet_folder)

    for subdir in subdirs:
        category_folder = os.path.join(shapenet_folder, subdir)

        # Create new directory for the ShapeNet category
        new_category_folder = os.path.join(new_folder, subdir)
        if not os.path.exists(new_category_folder):
            os.makedirs(new_category_folder)

        # copy prototype.urdf to subdir
        src_proto = os.path.join(shapenet_folder, '_prototype.urdf')
        dst_proto = os.path.join(new_category_folder, '_prototype.urdf')
        shutil.copy2(src_proto, dst_proto)

        builder = ObjectUrdfBuilder(new_category_folder)

        obj_paths = glob(os.path.join(category_folder, '*', 'models', '*.obj'))

        for obj_path in obj_paths:
            # Create new directory for the ShapeNet object
            new_object_folder = os.path.join(new_category_folder, obj_path.split(os.sep)[-3])
            if not os.path.exists(new_object_folder):
                os.makedirs(new_object_folder)

            if args.watertight:
                # Generate watertight mesh
                mesh = as_mesh(trimesh.load(obj_path))

                if mesh.is_watertight:
                    # Copy .obj to new directory
                    shutil.copy2(obj_path, os.path.join(new_object_folder, 'model.obj'))

                else:
                    vm, fm = pcu.make_mesh_watertight(mesh.vertices, mesh.faces, 50000)
                    watertight_path = os.path.join(new_object_folder, 'model.obj')
                    pcu.save_mesh_vf(watertight_path, vm, fm, dtype=np.float32)

            else:
                # Copy .obj to new directory
                shutil.copy2(obj_path, os.path.join(new_object_folder, 'model.obj'))

            # build urdf
            builder.build_urdf(filename=new_object_folder,
                               force_overwrite=True,
                               decompose_concave=False,
                               force_decompose=False,
                               center=None)

            # rename urdf with their .obj name
            src_urdf_path = glob(os.path.join(new_category_folder, '[!_]*.urdf'))[0]
            dst_urdf_path = os.path.join(new_object_folder, 'model.urdf')
            shutil.move(src_urdf_path, dst_urdf_path)

            # Add flag 'concave=yes' to allow concave meshes in simulators,
            # edit the new urdf with the updated mesh path
            obj_index = dst_urdf_path.split(os.sep)[-2]
            original = [f'filename=\"{obj_index}\"',
                        'collision']
            replacement = ['filename=\"model.obj\"',
                           'collision concave=\"yes\"']
            replace_in_file(dst_urdf_path, original, replacement)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--watertight", default=False, action='store_true', help="Extract watertight meshes and watertight URDF"
    )
    args = parser.parse_args()

    main(args)
