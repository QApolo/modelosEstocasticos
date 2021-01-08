from volumen_exca import VolumenExcavacion


from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt



if __name__ == '__main__':
    lado = 10
    ed = 0.2
    tn = [90.1, 90.1, 78.6, 79.0]
    sr = [63.5, 63.5, 63.5, 63.5]

    ve = VolumenExcavacion(lado, ed, tn, sr)
    print(ve.getHx())
    print(ve.getVolumen())


    ## ================= gráfica =================
    fig = plt.figure()
    ax = Axes3D(fig)

    x = [0,0,lado,lado]
    y = [0,lado,lado,0]
    z = sr[:]

    za = [a + abs(b) for a, b in zip(z, ve.getHx())]

    zb = tn[:]
    
    verts3 = [list(zip(x,y,zb))]

    ax.set_xlim3d(0, lado)
    ax.set_ylim3d(0,lado)
    ax.set_zlim3d(min(sr),max(zb))

    
    verts = [list(zip(x,y,z))]
    ax.add_collection3d(Poly3DCollection(verts))

    ax.scatter(x,y,z)
    ax.scatter(x,y,za)
    ax.scatter(x,y,zb)

    verts2 = [list(zip(x,y,za))]
    #ax.autoscale(False)
    ax.add_collection3d(Poly3DCollection(verts2, facecolors='g'))

  
    ax.add_collection3d(Poly3DCollection(verts3, facecolors='r'))
    plt.show()
