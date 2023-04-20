import os
import time
import random
import pybullet as p
import pybullet_data
import sys
import numpy as np
import argparse

from obj_urdfs import primitive_objects
from obj_urdfs import random_objects
from obj_urdfs import gibson_feelies
from obj_urdfs import gibson_glavens
from obj_urdfs import gibson_bellpeppers
from obj_urdfs import ycb_objects
from obj_urdfs import superquadric_objects
from obj_urdfs import google_scanned_objects
from obj_urdfs.egad import egad_train_set
from obj_urdfs.egad import egad_eval_set
from obj_urdfs.shapenet import ShapeNetCoreV2


# get the object set from arguments
parser = argparse.ArgumentParser()
parser.add_argument("-object_set",
                    type=str,
                    default='primitive',
                    help="""
                        Options:{
                        primitive, random, superquadric, ycb, google, feelies, glavens,
                        bellpeppers, egad_train, egad_eval, shapenet}"""
                    )
args = parser.parse_args()
object_set = args.object_set

# connect to pybullet and load a plane
p.connect(p.GUI)
p.setGravity(0, 0, -10)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane_id = p.loadURDF("plane.urdf")

# load an object
start_pos = [0, 0, 0.15]
start_orn = p.getQuaternionFromEuler([0, 0, 0])

# flags for performing certain tasks
auto_scale = False
draw_com = False
record = False

if object_set == 'primitive':
    data_path = primitive_objects.get_data_path()
    model_list = primitive_objects.get_object_list()

elif object_set == 'random':
    data_path = random_objects.getDataPath()
    model_list = random_objects.get_object_list()

elif object_set == 'ycb':
    data_path = ycb_objects.getDataPath()
    model_list = ycb_objects.get_object_list()

elif object_set == 'superquadric':
    data_path = superquadric_objects.getDataPath()
    model_list = superquadric_objects.get_object_list()

elif object_set == 'google':
    data_path = google_scanned_objects.getDataPath()
    model_list = google_scanned_objects.get_object_list()

elif object_set == 'feelies':
    data_path = gibson_feelies.getDataPath()
    model_list = gibson_feelies.get_object_list()

elif object_set == 'glavens':
    data_path = gibson_glavens.getDataPath()
    model_list = gibson_glavens.get_object_list()

elif object_set == 'bellpeppers':
    data_path = gibson_bellpeppers.getDataPath()
    model_list = gibson_bellpeppers.get_object_list()

elif object_set == 'egad_eval':
    data_path = egad_eval_set.getDataPath()
    model_list = egad_eval_set.get_object_list()

elif object_set == 'egad_train':
    data_path = egad_train_set.getDataPath()
    model_list = egad_train_set.get_object_list()

elif object_set == 'shapenet':
    data_path = ShapeNetCoreV2.getDataPath()
    model_list = ShapeNetCoreV2.get_object_list()
    start_orn = p.getQuaternionFromEuler([np.pi/2, 0, np.pi/2])

else:
    sys.exit('Incorrect object_set: {}'.format(object_set))


print('Number of objects in set: {}'.format(len(model_list)))


def reset(obj_id):

    # remove if already exists
    if obj_id is not None:
        p.removeBody(obj_id)

    # select rand file
    rand_file = random.choice(model_list)

    # load obj
    print('Loading: ', rand_file)
    # flags = p.URDF_INITIALIZE_SAT_FEATURES
    obj_id = p.loadURDF(
        os.path.join(data_path, rand_file, "model.urdf"),
        start_pos, start_orn,
        # flags=flags
    )

    if auto_scale:
        # Could use trimesh to get bounding box before loading in pybullet
        # to avoid remove/reload
        targ_diag = 0.15
        # targ_diag = 0.5
        obj_aabb = p.getAABB(obj_id)
        aabb_min, aabb_max = obj_aabb[0], obj_aabb[1]
        long_diag = np.linalg.norm(np.array(aabb_min)-np.array(aabb_max))

        ratio = targ_diag / long_diag
        p.removeBody(obj_id)
        obj_id = p.loadURDF(
            os.path.join(data_path, rand_file, "model.urdf"),
            start_pos, start_orn,
            # flags=flags,
            globalScaling=ratio
        )
    return obj_id


obj_id = reset(None)

# set camera position
cam_dist = 0.5
cam_roll = 0
cam_pitch = -30
cam_yaw = -45
cam_pos = [0, 0, 0]
p.resetDebugVisualizerCamera(cam_dist, cam_yaw, cam_pitch, cam_pos)

if record:
    import imageio
    fov = 60
    pixel_width, pixel_height = 256, 256
    near_plane, far_plane = 0.01, 100
    reset_every = 100
    save_every = 5
    max_steps = 2000
    saved_frames = []

# infinite loop of sim
step = 1
while True:
    p.stepSimulation()
    time.sleep(1./240.)

    if draw_com:
        p.addUserDebugLine([0, 0, 0], [0.1, 0, 0], [1, 0, 0], parentObjectUniqueId=obj_id, lifeTime=0.1)
        p.addUserDebugLine([0, 0, 0], [0, 0.1, 0], [0, 1, 0], parentObjectUniqueId=obj_id, lifeTime=0.1)
        p.addUserDebugLine([0, 0, 0], [0, 0, 0.1], [0, 0, 1], parentObjectUniqueId=obj_id, lifeTime=0.1)

    if record:
        if (step % save_every == 0):
            # get image from camera
            view_matrix = p.computeViewMatrixFromYawPitchRoll(cameraTargetPosition=cam_pos,
                                                              distance=cam_dist,
                                                              yaw=cam_yaw,
                                                              pitch=cam_pitch,
                                                              roll=cam_roll,
                                                              upAxisIndex=2)

            aspect = pixel_width / pixel_height
            projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, near_plane, far_plane)
            img_arr = p.getCameraImage(pixel_width,
                                       pixel_height,
                                       view_matrix,
                                       projection_matrix,
                                       renderer=p.ER_BULLET_HARDWARE_OPENGL,
                                       # renderer=p.ER_TINY_RENDERER,
                                       )
            rgb = img_arr[2]  # color data RGB

            saved_frames.append(rgb)

        if (step % reset_every == 0):
            reset(obj_id)

        step += 1
        if step == max_steps:
            break

    # press q to break
    q_key = ord('q')
    r_key = ord('r')
    keys = p.getKeyboardEvents()
    if q_key in keys and keys[q_key] & p.KEY_WAS_TRIGGERED:
        exit()
    elif r_key in keys and keys[r_key] & p.KEY_WAS_TRIGGERED:
        obj_id = reset(obj_id)

if record:
    print('Saving Figure...')
    imageio.mimsave(os.path.join('../figures', '{}_example.gif'.format(object_set)), saved_frames, fps=24)

p.disconnect()
