import os
from glob import glob
import pathlib

from pybullet_object_models.cleanup_tools import remove_empty_dirs, get_immediate_subdirectories
from google.protobuf import text_format as pbtf


def rename_google_scanned_objects(dir):

    subdirs = get_immediate_subdirectories(dir)

    item_name_list = []
    for old_name in subdirs:

        # print(old_name)
        old_path = os.path.abspath(os.path.join(dir, old_name))
        metadata_file = os.path.join(old_path, 'model/metadata.pbtxt')

        dirname = pathlib.Path(old_path).stem
        if dirname == '__pycache__':
            continue

        with open(metadata_file, 'r') as f:
            lines = f.readlines()
            item_name = lines[3].split(":", 1)[1].replace("\"", "").strip()

        # check if there is a duplicate name
        # only works for single duplicates
        if item_name in item_name_list:
            item_name = item_name + '_v2'
        item_name_list.append(item_name)

        # rename directory
        new_path = os.path.abspath(os.path.join(dir, item_name))
        if os.path.isdir(new_path):
            continue
        os.rename(old_path, new_path)


def move_google_textures(dir):

    path = pathlib.Path(dir).absolute()
    all_tex_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.png'))]

    for tex_file in all_tex_files:
        old_path = pathlib.Path(tex_file)
        model_path = old_path.parents[2]
        tex_name = old_path.name
        new_path = os.path.join(model_path, 'meshes', tex_name)

        print('Moving texture: {}'.format(old_path.parents[3].stem))
        os.rename(old_path, new_path)


if __name__ == '__main__':
    # dir = os.path.join("google_scanned_objects")
    dir = os.path.join("test_folder")

    rename_google_scanned_objects(dir)
    move_google_textures(dir)
    remove_empty_dirs(dir)
    remove_empty_dirs(dir)
