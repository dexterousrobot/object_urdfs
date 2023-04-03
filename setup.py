import os
from setuptools import setup, find_packages

setup_py_dir = os.path.dirname(os.path.realpath(__file__))
need_files = []
datadir = "obj_urdfs"

hh = os.path.join(setup_py_dir, datadir)

for root, dirs, files in os.walk(hh):
    for fn in files:
        ext = os.path.splitext(fn)[1][1:]
        if ext and ext in 'urdf sdf xml stl ini obj mtl png'.split():
            fn = root + "/" + fn
            need_files.append(fn[1 + len(hh):])

print("find_packages() \n {}".format(find_packages()))

setup(
  name="obj_urdfs",
  version="0.1",
  author="Alex Church",
  author_email="alex.church@bristol.ac.uk",
  description="URDF models of objects for simulation.",
  license="LGPL",
  python_requires='>=3',
  keywords="urdf model object simulation pybullet mujoco isaacgym obj shapenet ycb",
  package_dir={'': '.'},
  packages=find_packages(),
  package_data={'obj_urdfs': need_files},
)
