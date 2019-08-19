
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import copy
import math

fig, ax = plt.subplots()

n = 100
l = 15.0
xmin = -1
xmax = 1
ymin = -1
ymax = 1
buffer = 0
#is there a color bar
cb = True

#finds electric field strengths from the inputted point charges
def findField(x, y,charges):
    u,v = 0,0

    for i in range(0,len(charges[0])):

        eField = (9*10**9)*charges[2][i]/((charges[1][i]-y)**2+(charges[0][i]-x)**2)
        theta = np.arctan((charges[1][i]-y)/(charges[0][i]-x))
        e = (charges[0][i]-x)/abs(charges[0][i]-x)

        u+= eField * np.cos(theta) * e
        v+= eField * np.sin(theta) * e


    return (u),(v)

#updates positions
def updateClose(x1,buffer,ys):
    i = 0
    x2 = list(x1)
    while i<len(x2):
        for j in ys:
            if abs(x2[i]-j)<=buffer:

                x2[i]+=0.01
        i+=1
    return np.array(x2)

#reformats array so it's easier to use
def adjArray(U):
    a = 4
    L1 = list(U)
    a = sum(list(L1[0])) / float(len(list(L1[0])))
    a*=3
    i = 0
    while (i<len(L1)):
        L1[i] = list(L1[i])
        j = 0
        while j<len(L1[i]):

            if abs(L1[i][j])>a:
                L1[i][j] = a*L1[i][j]/abs(L1[i][j])
            j+=1
        L1[i] = np.array(L1[i])
        i+=1
    return np.array(L1)


def logArray(U,a):
    L1 = list(U)
    avg = sum(L1)/float(len(L1))
    i = 0
    while (i<len(L1)):
        L1[i] = list(L1[i])
        j = 0
        while j<len(L1[i]):
            L1[i][j] = math.log(L1[i][j],a)
            j+=1
        L1[i] = np.array(L1[i])
        i+=1
    return np.array(L1)

#animation function
def animate(i):
    global cb
    ax.clear()

    data = open('Data.txt', 'r').read()
    Vals = data.split('\n_____\n')
    ranges = Vals[0].split('\n')
    points = Vals[2].split('\n')
    charge = Vals[3]
    x, y = charge.split(',')
    dimensions = []
    for window in ranges:
        nothing, val = window.split('= ')
        dimensions.append(float(val))

    xs = []
    ys = []
    qs = []
    for point in points:
        if len(point) > 1:
            x, y, q= point.split(',')
            xs.append(float(x))
            ys.append(float(y))
            qs.append(-float(q)*10**-9)

    #from mins and maxes
    x1 = np.linspace(dimensions[0],dimensions[1],n)
    x2 = np.linspace(dimensions[2],dimensions[3],n)

    #create grid
    x1mesh,x2mesh = np.meshgrid(updateClose(x1,buffer,xs),updateClose(x2,buffer,ys))
    U,V = findField(x1mesh,x2mesh,[xs,ys,qs])
    hyp = np.hypot(U,V)
    S=adjArray(hyp)

    x1 = updateClose(x1,buffer,xs)
    x2 = updateClose(x2,buffer,ys)
    X1mesh, X2mesh = np.meshgrid(x1, x2)
    U2,V2 = findField(X1mesh,X2mesh,[xs,ys,qs])

    #creates stream lines
    stream = ax.streamplot(X1mesh, X2mesh, U2, V2, color = S, linewidth=1, cmap='cool')

    logS= logArray(S,100)
    #contour lines for voltage lines
    contour = ax.contour(X1mesh,X2mesh,logS,10,cmap = 'prism')

    #makes colorbar for reference to measure intensity
    if cb:
        fig.colorbar(contour)
        fig.colorbar(stream.lines)
        cb = False

    #plots point charges
    for item in range(len(xs)):
        if (qs[item]<0):
            plt.plot(xs[item], ys[item], 'ro', color = 'r')
        elif (qs[item]>0):
            plt.plot(xs[item], ys[item], 'ro', color = 'b')



ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()
