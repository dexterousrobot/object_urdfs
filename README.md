# Object URDFs

This repository contains a collection of object models for simulation, along with helper scripts for downloading, generating and tidying the required files.

The list of available objects includes:

- [Primitive Objects](#primitive-objects)
- [Random Objects](#random-objects)
- [Superquadric Objects](#superquadric-objects)
- [YCB Objects](#ycb-objects)
- [Google Scanned Objects](#google-scanned-objects)
- [Evolved Grasping Analysis Dataset (EGAD)](#egad-objects)
- [Gibson Objects](#gibson-objects)
- [ShapeNetCore.v2](#shapenetcorev2)

Each object has the following files:

  - Textured mesh for visualization (`.obj`).

  - Simplified mesh for collision (`.obj`). These meshes can be basic shapes or a V-HACD decomposition of the textured mesh, depending on the complexity of the object shape. These are generally generated using the [obj2urdf](https://github.com/cbteeple/object2urdf) package.

  - URDF file to load the object into the simulation.

  - **TODO: add accurate mass and dynamics values to urdfs where possible.**

### Setup ###

The repo requires a **python version >= 3**. It can be installed with pip by doing:

```bash
$ git clone https://github.com/dexterousrobot/object-urdfs.git
$ cd object_urdfs
$ pip install -e .
```

It has been tested only on Ubuntu 18.04 LTS.

### Primitive Objects ###

  - A set of simple objects created in blender.

<p align="center">
	<img width="240"  src="figures/primitive_example.gif">
</p>

### Random Objects ###

  - Set of randomly generated objects from the [pybullet repo](https://github.com/bulletphysics/bullet3/tree/master/examples/pybullet/gym/pybullet_data/random_urdfs).

<p align="center">
	<img width="240"  src="figures/random_example.gif">
</p>

### Superquadric Objects ###

  - Custom objects with a superquadric (superellipsoid) shape, generated using the [pygalmesh tool](https://github.com/nschloe/pygalmesh).

<p align="center">
	<img width="240"  src="figures/superquadric_example.gif">
</p>

  - Tools are provided for generating your own Superquadric object models. This requires using the [pygalmesh tool](https://github.com/nschloe/pygalmesh) which can be installed the tools by doing:

```bash
$ conda create -n env_pygalmesh python=3.8
$ conda activate env_pygalmesh
$ conda install -c conda-forge pygalmesh
$ pip install trimesh #this is used to interactively fix a bug in the generated meshes, related to the inverted surface normals
```

Using conda to install the tool is not probably the ideal option for some people but it is the best and easiest way at the moment, as pointed out in its [github repo](https://github.com/nschloe/pygalmesh).

We provide information about how to generate custom objects by using the pygalmesh tool.

1. Navigate to the `superquadric_objects` folder:

```bash
$ cd object_urdfs/object_urdfs/superquadric_objects/
```

2. Activate the conda pygalmesh environment:

```bash
$ conda activate /path/to/env_pygalmesh
```

3. Run the script to generate the meshes:
```bash
$ python generate_superquadric_mesh.py
```
  The output meshes are saved according to the following tree:
```bash
sq_l1_l2_l3_l4_l5/
└── model.obj
```

4. Run the script to generate the URDF model for each new superquadric object:
```
$ python generate_urdf_model.py
```
They are saved inside each superquadric object folder as follow:
```bash
sq_l1_l2_l3_l4_l5/
├── model.obj
└── model.urdf
```

The output meshes have a superquadric shape defined according to the `inside-outside` function:
```
F = ( (x / λ1) ** (2/λ5) + (y / λ2) ** (2/λ5) ) ** (λ5/λ4) + (z / λ3) ** (2/λ4)
```
By default, the `generate_superquadric_mesh.py` creates 100 superquadric meshes, with `λ4, λ5` varying in the range `(0.1, 1.9, step = 0.2)`

You can of course modify the script to reduce the number of generated superquadric meshes as you like.


### YCB Objects ###

  - The near full set of YCB objects available for download [here](https://www.ycbbenchmarks.com/object-models/).

<p align="center">
	<img width="240"  src="figures/ycb_example.gif">
</p>

  - This is too large to store in this repo (approx 1Gb), a tool for dowloading these objects is available [here](https://github.com/sea-bass/ycb-tools), a very slightly modified version of this script with a function for removing numbers from the directory names is included in this repo.

  - The downloaded files can then be copied to the `ycb_objects` directory within this repo. This should contain the downloaded files, along with `__init__.py` and `_prototype.urdf` for generating the urdf files using obj2urdf.

  - To generate urdf files from the downloaded .obj files run `build_object_urdfs.py` with the directoy name set correctly, this will also generate convex decompositions, more details are provided [here](https://github.com/cbteeple/object2urdf).

  - Additionally, there are 3 SDF files, each loading some YCB objects arranged according to a specific layout. The layouts reproduce the layouts of the [GRASPA-benchmark](https://github.com/robotology/GRASPA-benchmark). **TODO: fix broken orientations on layouts.**

### Google Scanned Objects ###

  - Over 1000 "common" household objects that have been 3D scanned for use in robotic simulation and synthetic perception research from [Google Research](https://app.ignitionrobotics.org/GoogleResearch/fuel/collections/Google%20Scanned%20Objects).

<p align="center">
	<img width="240"  src="figures/google_example.gif">
</p>

  - This is too large to store on this repo, the full set of objects can be downloaded using this [repo](https://github.com/tommymchugh/gso_downloader).

  - I have limited expierience with Bazel but what worked for me was

```bash
git clone https://github.com/tommymchugh/gso_downloader.git
cd gso_downloader/
bazel build ...
./bazel-bin/src/download
```
  - This started downloading all the required files into my home directory. **Warning, this is over 10GB**.

  - The downloaded files can then be copied to the `google_scanned_objects` directory within this repo. This should contain the downloaded files (in the numbered directories), along with `__init__.py` and `_prototype.urdf` for generating the urdf files using obj2urdf.

  - A script for renaming the directories, moving textures and clearing empty directories is provided in `tidy_google_objects.py`. Be careful when using as this will be removing/renaming a large number of files, I would reccomended commenting out any code that alters files and monitoring beforehand to make sure it is working as intended before use.

  - This comes with sdf files that can directly be used in most physics simulators, however for consistency I find automatically generating urdf files using the [obj2urdf](https://github.com/cbteeple/object2urdf) package helpful. A script to do this is provided in `build_object_urdfs.py` (change directoy name), this will also generate convex decompositions, more details are provided in the linked repo. **Warning, takes a while to run for the full google_scanned_objects set**.

### EGAD Objects ###

Evolved  Grasping  Analysis  Dataset (EGAD), comprising over 2000 generated objects aimed at training and evaluating robotic visual grasp detection algorithms. See more details [here](https://github.com/dougsm/egad) and [here](https://arxiv.org/abs/2003.01314).

<p align="center">
	<img width="240"  src="figures/egad_train_example.gif">
</p>

To set up these objects:

 - Follow the steps to download the objects available on the project website ([https://dougsm.github.io/egad/](https://dougsm.github.io/egad/)).

 - Place the extracted files in the egad directory under `egad/egad_train_set` and `egad/egad_eval_set`.

 - Run `python tidy_egad.py` to move all `.obj` files into their own directories.

 - Copy the `_protype.urdf` and `__init__.py` files from `/egad/` into the `egad_eval_set` and `egad_train_set` directories.

 - Run `python build_object_urdfs.py` with the correct directories uncommented. **Warning, this will take a while for the full 2000 object training set**.

 - Run `python demo_load_object.py -object_set=egad_eval` or `-object_set=egad_train` to check things work correctly.

### Gibson Objects ###

 - Sets of objects for visual and haptic shape perception (see [here](https://academics.skidmore.edu/blogs/flip/?page_id=669) for more info).

 <p align="center">
	<img width="240"  src="figures/glavens_example.gif">
</p>

 - [Feelies](https://github.com/skidvision/Feelies): Artificial shapes for vision and haptic experiments.

 - [Glavens](https://github.com/skidvision/Glavens): Shapes for haptic experiments of progressive complexity.

 - [BellPeppers](https://github.com/skidvision/Bellpeppers): Natural shapes for vision and haptic experiments

 - Some of the meshes have been simplified to reduce the number of triangles.

### ShapeNetCore.v2 ###

Please make sure to have the python library `point-cloud-utils` and `trimesh` installed. This ensures the etxraction of watertight meshes (if requires). Please read below for citation.

<p align="center">
	<img width="240"  src="figures/shapenet_example.gif">
</p>


- The dataset is available on the ShapeNet website ([https://shapenet.org/](https://shapenet.org/)).

To extract `.urdf` files from the `ShapeNetCoreV2` dataset, please follow these instructions:

1. Download the `ShapeNetCoreV2` dataset and place it under `object_urdfs/shapenet/`. This download defaults the dataset folder name as `ShapeNetCore.v2`. Please rename the folder as `ShapeNetCoreV2`.  

2. Copy the `_protype.urdf` and `__init__.py` files from `/egad/` under the `ShapeNetCoreV2` directory.

3. Once the previous two steps are completed, you should have the following tree:
```
object_urdfs
 ├── shapenet
 │   ├── ShapeNetCoreV2
 │   │   ├── _prototype.urdf
 │   │   ├── ...   # example: 02942699
 |   |   |   ├── ...    # example: 1ab3abb5c090d9b68e940c4e64a94e1e
```

4. In the project root folder, run `python build_shapenet_urdfs.py`. This generates a new folder called `ShapeNetCoreV2urdf`, which has the same structure as the original folder `ShapeNetCoreV2`. The script extracts `.urdf` files from the ShapeNet `.obj` files. The extracted files, renamed `model.urdf`, can be found under each object ID directory in the new folder. In addition, the original `model_normalized.obj` is copied to the new folder. For example:
```
object_urdfs
 ├── shapenet
 │   ├── ShapeNetCoreV2urdf  <-- new folder
 │   │   ├── _prototype.urdf
 │   │   ├── 02942699
 |   |   |   ├── 1ab3abb5c090d9b68e940c4e64a94e1e
 |   |   |   |   ├── model.urdf <-- EXTRACTED .URDF
 |   |   |   |   ├── model.obj
```

- Some applications require watertight meshes. An example is DeepSDF. If a watertight mesh is required, please run `python build_shapenet_urdfs.py --watertight`. This first generates a watertight mesh and then extract its urdf. The generated dataset has the same structure as described above, but `model.obj` and `model.urdf` are watertight.

### Usage ###

Example scripts for importing the objects into pybullet are provided in the examples folder. To run these cd into the `examples` directory and run `python demo_load_object.py`. Use the `-object_set=` argument to load from a given object set, currently this can be selected from `primitive`, `random`, `ycb`, `superquadric` or `google` if setup correctly.

We use the convention that the object name is the name of the directory, and the urdf file is titled `model.urdf`. The function `getDataPath()` and `getModelList()` can be used to help load objects. Here is a code snippet for importing objects.

```python
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
```

Here is a Python example to load the objects inside the pybullet simulation:

```python
import os
import time
import pybullet as p
import pybullet_data
from object_urdfs import ycb_objects

## Open GUI and set pybullet_data in the path
p.connect(p.GUI)
p.resetDebugVisualizerCamera(3, 90, -30, [0.0, -0.0, -0.0])
p.setTimeStep(1 / 240.)

## Load plane contained in pybullet_data
planeId = p.loadURDF(os.path.join(pybullet_data.getDataPath(), "plane.urdf"))

## Load the object
obj_id = p.loadURDF(os.path.join(ycb_objects.getDataPath(), 'banana', "model.urdf"), [1., 0.0, 0.8])

## Start pybullet loop
p.setGravity(0, 0, -9.8)
while 1:
    p.stepSimulation()
    time.sleep(1./240)
```

# Citation
If this library contributes to an academic publication, please consider citing the following resources:
```
@software{trimesh,
	author = {{Dawson-Haggerty et al.}},
	title = {trimesh},
	url = {https://trimsh.org/},
	version = {3.2.0},
	date = {2019-12-8},
}
```
If you have used the Shapenet URDF extraction tool:
```
@misc{point-cloud-utils,
  title = {Point Cloud Utils},
  author = {Francis Williams},
  note = {https://www.github.com/fwilliams/point-cloud-utils},
  year = {2022}
}
```
