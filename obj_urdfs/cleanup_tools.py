import os
from glob import glob
import pathlib
import time


def remove_empty_dirs(dir):
    subdirs = glob(dir + '/**/', recursive=True)
    n_empty, n_full = 0, 0
    for dir in subdirs:
        if len(os.listdir(dir)) == 0:
            n_empty += 1
            print('Removing: ', dir)
            os.rmdir(dir)
            time.sleep(0.001)
        else:
            n_full += 1
    print('Empty: ', n_empty)
    print('Full: ', n_full)


def remove_urdfs(dir):
    path = pathlib.Path(dir).absolute()
    all_urdf_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.urdf'))]
    for file_path in all_urdf_files:
        path = pathlib.Path(file_path)

        filename = path.stem
        if filename == '_prototype':
            continue

        os.remove(path)


def rename_urdfs(dir):
    path = pathlib.Path(dir).absolute()
    all_urdf_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.urdf'))]
    for file_path in all_urdf_files:
        path = pathlib.Path(file_path)
        new_path = os.path.join(path.parent.absolute(), 'model.urdf')

        filename = path.stem
        if filename == '_prototype':
            continue

        os.rename(path, new_path)


def get_immediate_subdirectories(a_dir):
    subdirs = [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]
    try:
        subdirs.remove('__pycache__')
    except:
        pass
    return sorted(subdirs)


def count_dirs(dir):
    subdirs = get_immediate_subdirectories(dir)
    print(len(subdirs))


def move_urdfs_to_subdirs(dir):
    """
    Move urdfs generated from object2urdf into the file directories
    """
    path = pathlib.Path(dir).absolute()
    all_urdf_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.urdf'))]

    for file_path in all_urdf_files:
        path = pathlib.Path(file_path)
        filename = path.stem

        if filename == '_prototype':
            continue

        new_path = os.path.join(path.parent.absolute(), filename, filename+'.urdf')

        # create new urdf in subdir with mesh filename changed to match new place
        with open(path, 'r') as read_file:
            with open(new_path, "w") as write_file:
                for line in read_file:
                    if 'filename' in line:
                        new_line = line.replace(filename+'/', '')
                        write_file.write(new_line)
                    else:
                        write_file.write(line)

        # remove old urdf file
        os.remove(path)


def simplify_mesh(dir):
    import open3d as o3d
    target_number_of_triangles = 16000

    path = pathlib.Path(dir).absolute()
    all_obj_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.obj'))]
    print(all_obj_files)
    for obj_file in all_obj_files:
        mesh = o3d.io.read_triangle_mesh(obj_file)

        voxel_size = max(mesh.get_max_bound() - mesh.get_min_bound()) / 64
        print(f'voxel_size = {voxel_size:e}')
        mesh_smp = mesh.simplify_vertex_clustering(
            voxel_size=voxel_size,
            contraction=o3d.geometry.SimplificationContraction.Average)

        mesh = o3d.io.write_triangle_mesh(obj_file, mesh_smp)


if __name__ == '__main__':
    remove_urdfs('test_folder')
