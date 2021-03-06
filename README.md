## FEApy
FEApy is a python-based finite element analysis framework for education and 
research purpose by Saad Tarek, Structural Engineering fresh graduate(2020 
class)...  contact me on twitter @leoiev or through the mail in examples section..
## Version
Current:1.0.0
## Requirements
Numpy is a must. Matplotlib is needed for visualization. Mpmath is needed for Matrix derivation.
## Installation
```
Using pip:
$pip install feon
```
Or
```
$python setup.py install 
```
## Packages
* sa---For structrual analysis
* ffa --- For fluid flow analysis
* derivation --- For element matrix derivation 

## Elements supported

* Spring1D11 
* Spring2D11
* Spring3D11

* Link1D11
* Link2D11
* Link3D11

* Beam1D11
* Beam2D11
* Beam3D11

* Tri2d11S---- Triange elements for plane stress problem
* Tri2D11 ---- Triange elements for plane strain problem
* Tetra3D11 
* Quad2D11S 
* Quad2D11
* Plate3D11 ---Midline plate
* Brick3D11

**We name the elements with "Name" + "dimension" + 'order" + "type", type 1 means elastic .**

## Examples

**A Beam Problem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/elements-introduction/beam1/screenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.sa import *

if __name__ == "__main__":
   E = 210e6
   A = 0.005
   I = 5e-5

   n0 = Node(0,0)
   n1 = Node(2,0)
   n2 = Node(4,0)
   n3 = Node(8,0)
   n4 = Node(10,0)

   e0 = Beam1D11((n0,n1),E,A,I)
   e1 = Beam1D11((n1,n2),E,A,I)
   e2 = Beam1D11((n2,n3),E,A,I)
   e3 = Beam1D11((n3,n4),E,A,I)

   s = System()
   s.add_nodes(n0,n1,n2,n3,n4)
   s.add_elements(e0,e1,e2,e3)

   for nd in [n0,n2,n3]:
       s.add_rolled_sup(nd.ID,"y")
   s.add_fixed_sup(4)
   s.add_element_load(2,"Q",-7)
   s.add_node_force(1,Fy = -10)
   s.solve()

   from feon.sa.draw2d import *
   for el in [e0,e1,e2]:
       draw_bar_info(el)


```
**A Beam3d problem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/elements-introduction/beam3/screenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.sa import *
from feon.tools import pair_wise
if __name__ == "__main__":

    E = 210e6
    G = 84e6
    A = 0.02
    I =[5e-5,10e-5,20e-5]

    n0 = Node(0,0,0)
    n1 = Node(0,4,0)
    n2 = Node(4,4,0)
    n3 = Node(0,4,0)

    n4 = Node(0,0,5)
    n5 = Node(0,4,5)
    n6 = Node(4,4,5)
    n7 = Node(0,4,5)

    n8 = Node(1,0,5)
    n9 = Node(3,0,5)

    nds1 = [n0,n3,n2,n1]
    nds2 = [n4,n7,n6,n5]
    nds3 = [n4,n8,n9,n7,n6,n5]
    els = []
    for nd in pair_wise(nds3,True):
       els.append(Beam3D11(nd,E,G,A,I))

    for i in range(4):
       els.append(Beam3D11((nds1[i],nds2[i]),E,G,A,I))


    s = System()
    s.add_nodes(nds1,nds3)
    s.add_elements(els)

    s.add_node_force(nds2[2].ID,Fx = -15)
    s.add_element_load(els[1].ID,"q",(0,-5))
    s.add_element_load(els[4].ID,"tri",(-10,0))

    s.add_fixed_sup([nd.ID for nd in nds1])
    s.solve()
   



    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import MultipleLocator
    noe = s.noe
    non = s.non

    N = np.array([el.force["N"] for el in els])
    N1 = N[:,0]
    N2 = N[:,1]
   
    Ty = np.array([el.force["Ty"] for el in els])
    Ty1 = Ty[:,0]
    Ty2 = Ty[:,1]

    Tz = np.array([el.force["Tz"] for el in els])
    Tz1 = Tz[:,0]
    Tz2 = Tz[:,1]

    Mx = np.array([el.force["Mx"] for el in els])
    Mx1 = Mx[:,0]
    Mx2 = Mx[:,1]

    My = np.array([el.force["My"] for el in els])
    My1 = My[:,0]
    My2 = My[:,1]

    Mz = np.array([el.force["Mz"] for el in els])
    Mz1 = Mz[:,0]
    Mz2 = Mz[:,1]


   
    fig1,fig2 = plt.figure(),plt.figure()
   
    ax1 = fig1.add_subplot(311)
    ax2 = fig1.add_subplot(312)
    ax3 = fig1.add_subplot(313)

    ax4 = fig2.add_subplot(311)
    ax5 = fig2.add_subplot(312)
    ax6 = fig2.add_subplot(313)
    
    ax3.set_xticks([-1,noe+1],1)
    ax3.set_xlabel(r"$Element ID$")
    ax1.set_ylabel(r"$N/kN$")
    ax2.set_ylabel(r"$Ty/kN$")
    ax3.set_ylabel(r"$Tz/kN$")
    ax3.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax2.xaxis.set_major_locator(MultipleLocator(1))
    ax2.set_ylim([-7,7])
   
    for i in range(noe):
       ax1.plot([i-0.5,i+0.5],[N1[i],N2[i]],"gs-")
       ax2.plot([i-0.5,i+0.5],[Ty1[i],Ty1[i]],"rs-")
       ax3.plot([i-0.5,i+0.5],[Tz1[i],Tz1[i]],"ks-")
       
    ax6.set_xticks([-1,noe+1],1)
    ax6.set_xlabel(r"$Element ID$")
    ax4.set_ylabel(r"$Mx/kNm$")
    ax5.set_ylabel(r"$My/kNm$")
    ax6.set_ylabel(r"$Mz/kNm$")
    ax6.xaxis.set_major_locator(MultipleLocator(1))
    ax4.xaxis.set_major_locator(MultipleLocator(1))
    ax5.xaxis.set_major_locator(MultipleLocator(1))
   
    for i in range(noe):
       ax4.plot([i-0.5,i+0.5],[Mx1[i],Mx2[i]],"gs-")
       ax5.plot([i-0.5,i+0.5],[My1[i],My2[i]],"rs-")
       ax6.plot([i-0.5,i+0.5],[Mz1[i],Mz2[i]],"ks-")

    plt.show()
```
**A Truss promblem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/problems/truss/screenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.sa import *
from feon.tools import pair_wise
from feon.sa.draw2d import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
if __name__ == "__main__":

    #material property
    E = 210e6 #elastic modulus 
    A1 = 31.2e-2 #cross-section area of hanging bars
    A2 = 8.16e-2 #cross-section area of others

    #create nodes and elements
    nds1 = []
    nds2 = []
    for i in range(13):
        nds1.append(Node(i,0))
    for i in range(11):
        nds2.append(Node(i+1,-1))
    els = []
    for e in pair_wise(nds1):
        els.append(Link2D11((e[0],e[1]),E,A1))
    for e in pair_wise(nds2):
        els.append(Link2D11((e[0],e[1]),E,A1))

    for i in range(6):
        els.append(Link2D11((nds1[i],nds2[i]),E,A2))
    for i in xrange(6):
        els.append(Link2D11((nds2[i+5],nds1[i+7]),E,A2))

    for i in range(11):
        els.append(Link2D11((nds1[i+1],nds2[i]),E,A2))

    #create FEA system
    s = System()

    
    #add nodes and elements into the system
    s.add_nodes(nds1,nds2)
    s.add_elements(els)

    #apply boundry condition
    s.add_node_force(nds1[0].ID,Fy = -1000)
    s.add_node_force(nds1[-1].ID,Fy = -1000)
    for i in range(1,12):
        s.add_node_force(nds1[i].ID,Fy = -1900)
    s.add_fixed_sup(nds1[0].ID)
    s.add_rolled_sup(nds1[-1].ID,"y")

    #solve the system
    s.solve()

    #show results
    disp = [np.sqrt(nd.disp["Ux"]**2+nd.disp["Uy"]**2) for nd in s.get_nodes()]
    
    eforce = [el.force["N"][0][0] for el in s.get_elements()]
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax.yaxis.get_major_formatter().set_powerlimits((0,1)) 
    ax2 = fig.add_subplot(212)
    ax2.yaxis.get_major_formatter().set_powerlimits((0,1)) 
    ax.set_xlabel(r"$Node ID$")
    ax.set_ylabel(r"$Disp/m$")
    ax.set_ylim([-0.05,0.05])
    ax.set_xlim([-1,27])
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.plot(range(len(disp)),disp,"r*-")
    ax2.set_xlabel(r"$Element ID$")
    ax2.set_xlim([-1,46])
    ax2.set_ylabel(r"$N/kN$")
    ax2.set_ylim(-40000,40000)
    ax2.xaxis.set_minor_locator(MultipleLocator(1))
    for i in range(len(eforce)):
        ax2.plot([i-0.5,i+0.5],[eforce[i],eforce[i]],"ks-",ms = 3)
    plt.show()
    draw_bar_info(els[5])
    

    
```
**Frame with hinged node problem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/problems/frame%20with%20hinged%20node/creenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.sa import *
from feon.tools import pair_wise

#define beamlink element
class BeamLink2D11(StructElement):
    def __init__(self,nodes,E,A,I):
        StructElement.__init__(self,nodes)
        self.E = E
        self.A = A
        self.I = I

    #define node degree of freedom, left node has three dofs
    #while the right node has only two
    def init_unknowns(self):
        self.nodes[0].init_unknowns("Ux","Uy","Phz")
        self.nodes[1].init_unknowns("Ux","Uy")
        self._ndof = 3

    #transformative matrix
    def calc_T(self):
        TBase = _calc_Tbase_for_2d_beam(self.nodes)
        self._T = np.zeros((6,6))
        self._T[:3,:3] = self._T[3:,3:] = TBase

    #stiffness matrix
    def calc_ke(self):
        self._ke = _calc_ke_for_2d_beamlink(E = self.E,A = self.A,I = self.I,L = self.volume)

def _calc_ke_for_2d_beamlink(E = 1.0,A = 1.0,I = 1.0,L = 1.0):
    a00 = E*A/L
    a03 = -a00
    a11 = 3.*E*I/L**3
    a12 = 3.*E*I/L**2
    a14 = -a11
    a22 = 3.*E*I/L
    T = np.array([[a00,  0.,   0.,  a03,  0.,0.],
                  [ 0., a11,  a12,  0., a14, 0.],
                  [ 0., a12,  a22,  0.,-a12, 0.],
                  [a03,  0.,   0., a00,  0., 0.],
                  [ 0., a14, -a12,  0., a11, 0.],
                  [ 0.,  0.,    0.,  0., 0., 0.]])
    return T
    
def _calc_Tbase_for_2d_beam(nodes):
    
    x1,y1 = nodes[0].x,nodes[0].y
    x2,y2 = nodes[1].x,nodes[1].y
    le = np.sqrt((x2-x1)**2+(y2-y1)**2)

    lx = (x2-x1)/le
    mx = (y2-y1)/le
    T = np.array([[lx,mx,0.],
                  [-mx,lx,0.],
                  [0.,0.,1.]])
                  
    return T

if __name__ == "__main__":
    #materials
    E = 210e6
    A = 0.005
    I = 10e-5

    #nodes and elements
    n0 = Node(0,0)
    n1 = Node(0,3)
    n2 = Node(4,3)
    n3 = Node(4,0)
    n4 = Node(4,5)
    n5 = Node(8,5)
    n6 = Node(8,0)
    e0 = Beam2D11((n0,n1),E,A,I)
    e1 = BeamLink2D11((n1,n2),E,A,I)
    e2 = Beam2D11((n2,n3),E,A,I)
    e3 = Beam2D11((n2,n4),E,A,I)
    e4 = Beam2D11((n4,n5),E,A,I)
    e5 = Beam2D11((n5,n6),E,A,I)
    
    #system
    s = System()
    s.add_nodes([n0,n1,n2,n3,n4,n5,n6])
    s.add_elements([e0,e1,e2,e3,e4,e5])
    s.add_node_force(1,Fx = -10)
    s.add_node_force(5,Fx = -10)
    s.add_fixed_sup(0,3,6)
    s.solve()

    print n2.disp
    print e1.force
    
    
```

**Embedded wall problem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/problems/embedded%20wall/screenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.sa import *
from feon.tools import pair_wise
import matplotlib.pyplot as plt
from feon.sa.draw2d import *
if __name__ == "__main__":
    #material
    E1 = 2.85e6 #elastic modulus of the wall 
    E2 = 200e6 #elastic modulus of the bracing
    k = 15000 #soil reaction coefficient 
    I = 0.0427 #inertia of the wall
    A = 0.8 # area of the wall section
    A1 = 0.003 #area of the bracing section
    ka = 0.6 #active earth pressure coefficient 

    #create nodes
    nds1 =[Node(0,-i) for i in range(10)]
    nds2 = [Node(0,-(i+20)*0.5) for i in range(11)]
    nds3 = [Node(-0.5,-(i+20)*0.5) for i in range(11)]
    nds4 = [Node(-1.5,-2),Node(-1.5,-6)]

    #create beam
    els=[]
    for nd in pair_wise(nds1+nds2):
        els.append(Beam2D11(nd,E1,A,I))

    
    #create soil spring
    for i in range(11):
        els.append(Spring2D11((nds2[i],nds3[i]),k))
        
    #create bracing 
    els.append(Link2D11((nds4[0],nds1[2]),E2,A1))
    els.append(Link2D11((nds4[1],nds1[6]),E2,A1))

    
    #create FEA system    
    s = System()
    s.add_nodes(nds1,nds2,nds3,nds4)
    s.add_elements(els)

    nid1 = [nd.ID for nd in nds3]
    nid2 = [nd.ID for nd in nds4]

    #add fixed supports
    s.add_fixed_sup(nid1,nid2)
    for i,el in enumerate(els[:10]):
        s.add_element_load(el.ID,"tri",-18*ka)
        s.add_element_load(el.ID,"q",-i*18*ka)

    #add active earth pressure
    for el in els[10:20]:
        s.add_element_load(el.ID,"q",-180*ka)

    for nd in nds1:
        nd.set_disp(Uy =0)

    for nd in nds2:
        nd.set_disp(Uy = 0)

    
    #solve the FEA system
    s.solve()

    #show results
    disp = np.array([nd.disp["Ux"] for nd in nds1]+[nd.disp["Ux"] for nd in nds2])*1000
    Mz = [el.force["Mz"][0][0] for el in els[:20]]

    fig1,fig2,fig3 = plt.figure(),plt.figure(),plt.figure()
    ax1 = fig1.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    ax3 = fig3.add_subplot(111)
    
    Y1 = [-i for i in range(10)]+[-(i+20)*0.5 for i in range(11)]
    Y2 = [-i-0.5 for i in range(10)]+[-(i+20)*0.5-0.5 for i in range(10)]
    ax1.plot(disp,Y1,"r--")
    ax1.set_xlabel("$Ux/mm$")
    ax1.set_ylabel("$Height/m$")
    ax2.plot(Mz,Y2,"r-+")
    ax2.set_xlabel("$Mz/kN.m$")
    ax2.set_ylabel("$Height/m$")

    for el in els[:20]:
        draw_element(ax3,el,lw = 10,color = "g")
        
    for el in els[20:31]:
        draw_spring(ax3,el,color = "k")

    for el in els[31:]:
        draw_element(ax3,el,lw = 1.5,color = "k",marker = "s")

    for nd in nds3+nds4:
        draw_fixed_sup(ax3,nd,factor = (0.4,4),color ="k")
    
    ax3.set_xlim([-2,2])
    ax3.set_ylim([-16,1])
    plt.show()

```
**Fuild flow problem**
![image](https://github.com/saadtareq/simple-FEA-py-/blob/master/examples/problems/fluid%20flow/screenshot.png)
```python
# -*- coding: utf-8 -*-
# ------------------------------------
#  Author: Saad Tarek
#  E-mail: sa3dtareq@gmail.com
#  License: FREE
# -------------------------------------

from feon.ffa import *
from feon.tools import pair_wise
import numpy as np
if __name__ == "__main__":

    #permeability 
    Kxx = -2e-5

    #create nodes and elements
    A = np.pi*(np.linspace(0.06,0.15,7)[:-1]+0.0075)
    nds = [Node(-i*0.1,0) for i in range(7)]
    els = []
    for i in range(6):
        els.append(E1D((nds[i],nds[i+1]),Kxx,A[i]))

    #create FEA system

    s = System()
    s.add_nodes(nds)
    s.add_elements(els)
    
    s.add_node_head(0,0.2)
    s.add_node_head(6,0.1)
    s.solve()

    print [nd.head["H"] for nd in nds]
    print [el.velocity["Vx"] for el in els]
```
