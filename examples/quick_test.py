import os
import random

# from obj_urdfs import primitive_objects as objects
# from obj_urdfs import random_objects as objects
# from obj_urdfs import gibson_feelies as objects
# from obj_urdfs import gibson_glavens as objects
# from obj_urdfs import gibson_bellpeppers as objects
# from obj_urdfs import ycb_objects as objects
# from obj_urdfs import superquadric_objects as objects
# from obj_urdfs import google_scanned_objects as objects
# from obj_urdfs.egad import egad_train_set as objects
# from obj_urdfs.egad import egad_eval_set as objects
from obj_urdfs.shapenet import ShapeNetCoreV2 as objects

# Get the path to the objects inside each package
data_path = objects.get_data_path()
object_list = objects.get_object_list()

# from which an object can be selected
rand_object_name = random.choice(object_list)

# the full path is then
path_to_urdf = os.path.join(data_path, rand_object_name, "model.urdf")

print("")
print("Data Path: ", data_path)
print("")
print("Object List", object_list)
print("")
print("URDF Path: ", path_to_urdf)
print("")
