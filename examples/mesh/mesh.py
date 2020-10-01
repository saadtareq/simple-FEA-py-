# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.mesh import Mesh

if __name__ == "__main__":
    mesh = Mesh()
    mesh.build(mesh_type = "rect",x_lim = [0,2],y_lim = [0,2],size = [2,2])
    print (mesh)
    print (mesh.points)
    print (mesh.elements)
    
    
