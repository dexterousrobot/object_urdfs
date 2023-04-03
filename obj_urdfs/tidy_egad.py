import os
from glob import glob
import pathlib


def move_obj_to_subdirs(dir):
    path = pathlib.Path(dir).absolute()
    all_obj_files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.obj'))]

    for file_path in all_obj_files:
        path = pathlib.Path(file_path)
        filename = path.stem

        new_dir = os.path.join(path.parent.absolute(), filename)
        os.makedirs(new_dir)

        new_path = os.path.join(new_dir, filename + '.obj')
        os.rename(path, new_path)


move_obj_to_subdirs('egad/egad_eval_set')
move_obj_to_subdirs('egad/egad_train_set')
