import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt


def b_spline(x,y,closed):
    if closed:
        # for a closed curve
        x = np.append(x,[x[0]])  
        y = np.append(y,[y[0]])

    l=len(x)  

    t=np.linspace(0,1,l-2,endpoint=True)
    t=np.append([0,0,0],t)
    t=np.append(t,[1,1,1])

    tck=[t,[x,y],3]
    u3=np.linspace(0,1,(max(l*2,70)),endpoint=True)
    return interpolate.splev(u3,tck)


if __name__ == '__main__':
    ctr = np.array( [(3.5 , 4), (2.5, 4.5), (1.5, 4), (1.0, 3.5),
                    (0, 2), (-0.5, 1.0), (-1.0, 0), (-1.5, -2), (-3, -1),])
    x = ctr[:,0]
    y = ctr[:,1]
    out = b_spline(x,y,False)
    plt.plot(x,y,'k--',label='Control polygon',marker='o',markerfacecolor='red')
    #plt.plot(x,y,'ro',label='Control points only')
    plt.plot(out[0],out[1],'b',linewidth=2.0,label='B-spline curve')
    plt.legend(loc='best')
    plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
    plt.title('Cubic B-spline curve evaluation')
    plt.show()

