import numpy as np
import matplotlib.pylab as plt
from matplotlib.animation import FuncAnimation

class Ising(object):
    
    #Constructor for Ising class. Creates an array of zeros and then fills it with +1 or -1 spins randomly. User inputted temp and dimensions are also made into instance variables.
    def __init__(self,temp,dimension,initial):
        if initial == True:
            self.array = np.random.choice([-1,1],size=(dimension,dimension))
        elif initial == False:
            self.array = np.ones(shape=(dimension,dimension))
        self.temp = temp
        self.dimension = dimension
        self.N = dimension*dimension

#Returns spins of nearest neighbours imposing Periodic Boundary Conditions. NN's are labelled nn1,nn2,nn3,nn4 and are up,down,right,left respectively.
    def NN_PBC(self,i,j):
        max = self.array.shape[0] - 1
        
        if i-1 < 0: nn1 = self.array[max,j]
        else: nn1 = self.array[i-1,j]

        if i+1 > max: nn2 = self.array[0,j]
        else: nn2 = self.array[i+1,j]
    
        if j+1 > max: nn3 = self.array[i,0]
        else: nn3 = self.array[i,j+1]
    
        if j-1 <0: nn4 = self.array[i,max]
        else: nn4 = self.array[i,j-1]
    
        return [nn1,nn2,nn3,nn4]

#Calculates the energy difference if a spin of index i,j is flipped
    def Energy_Calc(self,i,j):
        nns = np.sum(self.NN_PBC(i,j))
        E = 2*(self.array[i,j])*nns
        return E

#Instance method to carry out a single sweep using Glauber dynamics. Randomly chooses indices, calculates the energy difference if the spin is flipped. Does the flip depending on the Boltzmann probability.
    def Glauber_Sweep(self,iterations):

        for i in range(iterations):
            a = int(np.random.uniform(0,self.dimension))
            b = int(np.random.uniform(0,self.dimension))
            dE = self.Energy_Calc(a,b)
            
            r = np.random.uniform()
            p = np.exp(-dE/self.temp)
            if dE < 0:
                self.array[a,b] = -1 * self.array[a,b]
            elif p > r:
                self.array[a,b] = -1 * self.array[a,b]

#Instance method to carry out a single sweep using Kawasaki Dynamics. Randomly chooses 2 pairs of indices, calculates the energy difference if the spins are switched. Does the flip depending on the Boltzmann probability.
    def Kawasaki_Sweep(self,iterations):
        for i in range(iterations):
            a = int(np.random.uniform(0,self.dimension))
            b = int(np.random.uniform(0,self.dimension))
            c = int(np.random.uniform(0,self.dimension))
            d = int(np.random.uniform(0,self.dimension))
            
            #Only if the spins of the two randomly selected indices are NOT the same, the sweep is carried out.
            if not self.array[a,b] == self.array[c,d]:
                dE = self.Energy_Calc(a,b) + self.Energy_Calc(c,d)
                
                #If the selected pairs are nn's then an additional energy of 4 is added to dE
                if a+1==c and b==d: dE+=4
                elif a-1==c and b==d: dE+=4
                elif a==c and b+1==d: dE+=4
                elif a==c and b-1==d: dE+=4
            
                r = np.random.uniform()
                p = np.exp(-dE/self.temp)
            
                if dE < 0:
                    self.array[a,b],self.array[c,d] = self.array[c,d],self.array[a,b]
                elif p>r:
                    self.array[a,b],self.array[c,d] = self.array[c,d],self.array[a,b]

#Instance method which calculates the magnetization or squared magnetization of the Ising system if sq is equal to False or True respectively.
    def Measure_Mag(self,sq):
        if sq == False:
            m = np.abs(self.array.sum())
        elif sq == True:
            m = (self.array.sum())**2
        return m

#Instance method which is given lists of magnetization and magnetization squared and calculates the magnetic susceptibility.
    def Susceptibility(self,mlist,m2list):
        avg_m = np.average(mlist)
        avg_m2 = np.average(m2list)
        X = (avg_m2 - avg_m**2)/(self.temp*self.N)
        return avg_m, X

#Instance method which calculates the energy and squared energy of the system. Only uses the 2nd and 3rd nearest neighbours from list of 4 to prevent double counting.
    def Measure_Energy(self):
        E = 0.0
        for i in range(self.dimension):
            for j in range(self.dimension):
                nns = self.NN_PBC(i,j)
                dE = -1*self.array[i,j]*(nns[1]+nns[2])
                E += dE
        
        E2 = E**2
        return E, E2

#Instance method which takes energy and squared energy lists and calculates the Heat Capacity per Spin
    def Heat_Capacity(self,Elist,E2list):
        avg_E = np.average(Elist)
        avg_E2 = np.average(E2list)
        CvN = (avg_E2 - avg_E**2)/(self.N*(self.temp**2))
        return avg_E,CvN






