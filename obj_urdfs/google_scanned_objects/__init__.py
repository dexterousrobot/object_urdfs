import os
import sys


def get_data_path():
    resdir = os.path.join(os.path.dirname(__file__))
    subdirs_exist = any(os.path.isdir(os.path.join(resdir, i)) for i in os.listdir(resdir) if i != '__pycache__')
    if not subdirs_exist:
        sys.exit('Warning, no models exist for object set located ({}). Check they are dowloaded correctly.'.format(resdir))
    return resdir


def get_object_list():
    data_path = get_data_path()
    model_list = [os.path.basename(os.path.normpath(f.path)) for f in os.scandir(data_path) if f.is_dir()]
    try:
        model_list.remove('__pycache__')
    except ValueError:
        pass
    return model_list


def get_mesh_str():
    return "{filename}/model/meshes/model.obj"


def get_urdf_str():
    return "{filename}/model.urdf"


def get_urdf_scale():
    return [1.0, 1.0, 1.0]
