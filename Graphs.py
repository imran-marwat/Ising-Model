import numpy as np
import matplotlib.pylab as plt
import sys
from Ising_Class import Ising

#Define user defined variables: temperature, dimension of square lattic and choice of Glauber or Kawasaki Dynamics
temp = float(sys.argv[1])
dimension = int(sys.argv[2])
dynamics = sys.argv[3]

#Define empty global lists
E_list = []
Cv_list = []
M_list = []
X_list = []
temp_list = []

#Open a text file for writing data to
f = open('DataFile'+str(dynamics)+'.txt','w')

#If Glauber dynamics are selected Ising model is initialised from equilibirum (all aligned). Else if Kawasaki dynamics are selected model is initialised from random
if dynamics == "glauber":
    B = Ising(temp,dimension,initial=False)
elif dynamics == "kawasaki":
    B = Ising(temp,dimension,initial=True)


temp_timer = 0
#Perform simulation for 30 increments of temperature from 1K to 4K
for i in np.linspace(1,4,30):
    #Set temperature of instance B to i so the array does not need to be reinitialised each time
    B.temp = i
    temp_list.append(i)
    print(str(temp_timer)+" is the global timer")
    sweeps = 0
    #Define energy and magnetisation lists to calculate Cv and X from. To be cleared for each temperature
    m_list = []
    m2_list = []
    e_list = []
    e2_list = []
    
    #Number of iterations (hard-coded) of user's choice of dynamics
    for j in range(3000):
        if dynamics == "glauber":
            B.Glauber_Sweep(2500)
        if dynamics == "kawasaki":
            B.Kawasaki_Sweep(2500)
        
        #Conditions at which measurements of energy and magnetisation of the system are made
        if sweeps >= 200:
            if sweeps%10 == 0:
                m_list.append(B.Measure_Mag(sq=False))
                m2_list.append(B.Measure_Mag(sq=True))
                e,e2 = B.Measure_Energy()
                e_list.append(e)
                e2_list.append(e2)
        sweeps += 1

    #Average mag, X, avg E and Cv are calculated (both were calculated with Susceptibility method due to an early error which has now been resolved)
    avg_mag, X = B.Susceptibility(m_list,m2_list)
    avg_E, CvN = B.Susceptibility(e_list,e2_list)

    #The temperature, avg E, avg Cv, avg M and avg X are written to the data file
    f.write("{0:1.2}".format(B.temp)+" "+str(avg_E)+" "+str(CvN)+" "+str(avg_mag)+" "+str(X)+"\n")

    #Values appended to global lists for plotting
    E_list.append(avg_E)
    Cv_list.append(CvN/B.temp)
    M_list.append(avg_mag)
    X_list.append(X)
    temp_timer += 1

#Text file closed
f.close()

#All graphs plotted and saved as .png files
plt.plot(temp_list,E_list)
plt.xlabel("Temperature (K)")
plt.ylabel("<E>")
plt.title("Plot of the average Energy as a function of Temperature (K)")
plt.savefig('Energy'+str(dynamics)+'.png')
plt.show()

plt.plot(temp_list,Cv_list)
plt.xlabel("Temperature (K)")
plt.ylabel("Cv/N")
plt.title("Plot of the average Heat Capacity per Spin as a function of Temperature (K)")
plt.savefig('HeatCapacity'+str(dynamics)+'.png')
plt.show()

plt.plot(temp_list,M_list)
plt.xlabel("Temperature (K)")
plt.ylabel("<M>")
plt.title("Plot of the average Magnetisation as a function of Temperature (K)")
plt.savefig('Magnetisation'+str(dynamics)+'.png')
plt.show()

plt.plot(temp_list,X_list)
plt.xlabel("Temperature (K)")
plt.ylabel("X")
plt.title("Plot of the average Susceptibility as a function of Temperature (K)")
plt.savefig('Susceptibility'+str(dynamics)+'.png')
plt.show()





