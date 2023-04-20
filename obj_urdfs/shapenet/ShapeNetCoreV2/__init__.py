import os
import sys

from obj_urdfs.cleanup_tools import get_immediate_subdirectories


def get_data_path():
    resdir = os.path.join(os.path.dirname(__file__))
    subdirs_exist = any(os.path.isdir(os.path.join(resdir, i)) for i in os.listdir(resdir) if i != '__pycache__')
    if not subdirs_exist:
        sys.exit('Warning, no models exist for object set located ({}). Check they are dowloaded correctly.'.format(resdir))
    return resdir


def get_object_list():
    data_path = get_data_path()
    subdirs = get_immediate_subdirectories(data_path)
    model_list = []
    for subdir in subdirs:
        par_drive = os.path.join(data_path, subdir)
        models = [os.path.join(subdir, name) for name in os.listdir(par_drive) if os.path.isdir(os.path.join(par_drive, name))]
        model_list.extend(models)
    return model_list


def get_mesh_str():
    return "{filename}/{filename}.obj"


def get_urdf_str():
    return "{filename}/model.urdf"


def get_urdf_scale():
    return [0.1, 0.1, 0.1]
