"""
Pursuit of domain coloring to do Visual Quantum Mechanics. 

Modified  By   Reason
--------  --   ------
27-Aug-23 CBL  Original

References:

https://notebook.community/empet/Math/DomainColoring
http://docs.enthought.com/mayavi/mayavi/mlab.html


"""
from mayavi import mlab

def HSVcolormap():
    """
    defines colormap for analytic landscape
    """
    argum = np.linspace(-np.pi, np.pi, 256) 
    
    H = argum / (2*np.pi) + 1
    H = np.mod(H,1)
    S = np.ones(H.shape)
    V = np.ones(H.shape)
    
    HSV = np.dstack((H,S,V))
    RGB = hsv_to_rgb(HSV) 
   
    colormap = 255 * np.squeeze(RGB) 
    return colormap

def alandscape(rez, imz, argfz, modfz):
    """
    draws the (log)analytic landscape using the HSVcolormap
    """
   
    colormap = HSVcolormap() 
    mesh = mlab.mesh(rez, imz, modfz, scalars=argfz, vmin=-np.pi, vmax=np.pi) 
    
    LUT = mesh.module_manager.scalar_lut_manager.lut.table.to_array() 
    for k in range(3):
        LUT[:, k] = colormap[:,k] 
     
    mesh.module_manager.scalar_lut_manager.lut.table = LUT
    mlab.draw() 
    return mesh

def evalfun(f, re=[-2,2], im=[-2,2], N=50):
    """
    evaluates the log(|f|) at the points of a greed
    """
    nrx = N * (re[1]-re[0])
    nry = N * (im[1]-im[0])
    x = np.linspace(re[0], re[1], int(nrx))
    y = np.linspace(im[0], im[1], int(nry))
    
    x, y = np.meshgrid(x, y)
    z = x + 1j*y
    w = f(z)
    w[np.isinf(w)] = np.nan
    #m = np.absolute(w) # depending on the function f we can use one of these two versions for computing the module m
    m = np.log(np.absolute(w))
    return x, y, np.angle(w), m

mlab.figure(1, bgcolor=(0.95,0.95,0.95))
x,y, theta, m=evalfun(lambda z: (z**3-1)/z)
alandscape(x, y, theta, m) 
mlab.savefig('loglandsc1.jpg' )
