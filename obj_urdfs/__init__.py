from obj_urdfs import primitive_objects
from obj_urdfs import random_objects
from obj_urdfs import gibson_feelies
from obj_urdfs import gibson_glavens
from obj_urdfs import gibson_bellpeppers
# from obj_urdfs import ycb_objects
# from obj_urdfs import superquadric_objects
# from obj_urdfs import google_scanned_objects
# from obj_urdfs.egad import egad_train_set
# from obj_urdfs.egad import egad_eval_set
# from obj_urdfs.shapenet import ShapeNetCoreV2

objset_map = {
    'primitive': primitive_objects,
    'random': random_objects,
    'gibson_feelies': gibson_feelies,
    'gibson_glavens': gibson_glavens,
    'gibson_bellpeppers': gibson_bellpeppers,
    # 'ycb': ycb_objects,
    # 'superquadric': superquadric_objects,
    # 'google_scanned': google_scanned_objects,
    # 'egad_train': egad_train_set,
    # 'egad_eval': egad_eval_set,
    # 'shapenet': ShapeNetCoreV2,
}
