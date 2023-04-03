import os
import pygalmesh
import meshio
import trimesh
import time

t0 = time.time()

shape_values = [i/10 for i in range(1, 20, 2)]
l1 = l2 = l3 = 0.12

counter = 0
for l5 in shape_values:
    for l4 in shape_values:

        obj_dir = "sq_" + str(l1) + "_" + str(l2) + "_" + str(l3) + "_" + str(l4) + "_" + str(l5)
        os.makedirs(obj_dir, exist_ok=True)

        class SQ(pygalmesh.DomainBase):
            def __init__(self):
                super().__init__()

            def eval(self, x):
                return (((x[0] / l1) ** 2) ** (1/l5) + ((x[1] / l2) ** 2) ** (1/l5)) ** (l5/l4) \
                        + ((x[2] / l3) ** 2) ** (1/l4) - 1

            def get_bounding_sphere_squared_radius(self):
                return 0.5

        d = SQ()

        mesh = pygalmesh.generate_surface_mesh(
            d,
            min_facet_angle=30,
            max_radius_surface_delaunay_ball=0.005,
            max_facet_distance=0.005
        )

        meshio.write(os.path.join(obj_dir, "model.obj"), mesh, file_format="obj")

        # check normal issue with trimesh
        mesh_1 = trimesh.load_mesh(os.path.join(obj_dir, "model.obj"))
        mesh_1.show()
        cmd = input("Shape {}: invert? y/n... ".format(counter))
        if cmd == 'y':
            mesh_1.invert()
        mesh_1.export(os.path.join(obj_dir, "model.obj"))

        counter += 1

t1 = time.time()

print("elapsed time {}".format(round(t1 - t0, 4)))
