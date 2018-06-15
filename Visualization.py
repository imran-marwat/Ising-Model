import numpy as np
import sys
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation
from Ising_Class import Ising

#Create instance of Ising class
A = Ising(float(sys.argv[1]),int(sys.argv[2]),initial=True)

#Animation Function
def UpdatePlot(*args):
    image = ax.imshow(A.array)
    if dynamics == "glauber":
        A.Glauber_Sweep(2500)
    elif dynamics == "kawasaki":
        A.Kawasaki_Sweep(2500)
    return image,

#Perform 2500 sweeps prior to animation.
if sys.argv[3] == "glauber":
    A.Glauber_Sweep(2500)
elif sys.argv[3] == "kawasaki":
    A.Kawasaki_Sweep(2500)

#Calls animation function. User must close animation to end program.
fig,ax = plt.subplots()
image = ax.imshow(A.array)
ani = FuncAnimation(fig,UpdatePlot,blit=True)
plt.title("2D Ising Model Numerical Solution")
plt.xlabel("x coordinate")
plt.ylabel("y coordinate")
plt.show()
