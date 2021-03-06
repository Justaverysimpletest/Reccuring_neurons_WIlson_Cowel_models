#The following code is a modeling of the interaction of 2 populations of reccurent neurons. The equations
#and the bibliography were acquired from the book "theoretical neuroscience computational and mathematical 
#modeling of neural systems" from Peter Dayan & L.F. Abott along with some tutorials from "neuromatchacademy.io
import matplotlib.pyplot as plt
import numpy as np
import cmath

#time parameters
dt = 0.1 
T = 1000 
steps= int(T/dt) 
time = np.linspace(0,T,steps+1)

#1.parameters for excitatory population

IE=20         #external input
TauE = 10     #time constant(μs)
WEE = 1.25    #reccuring weight 
gammaE= -10   #noise (Hz)

#2.parameters for inhibitory population

II=10         #external input 
TauI= 20      #time constant(μs)
WII = -1       #reccuring weight
gammaI = 10   #noise (Hz)


#3.parameters for the populations interaction 
#first letter corresponds to the postsynaptic neuron/last letter to the presynaptic
WEI= -1      #interactive weight  
WIE=  1      #interactive weight 

#Initialisation of populations' firing rate {0-1}
rE = np.zeros(steps+1)
rI = np.zeros(steps+1)
rE[0]=  0.35
rI[0]=  0.35

#4.Define activation functions
#We will define here only sigmoid and ReLu

def ReLu(x): 
  return np.maximum(0,x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

#5. Calculation of firing rate over time for both populations of neurons and Plotting
#before oscilatory behavior occurence. We know that oscillatory occurs approximately  
#when TauI=40 so to plot the behaviour after oscillatory we just need to change the
#TauI value to a higher value.
#The for loop is analytically solving the differential equation that describes the  
#populations of the neurons

for t in range(0,steps): 
  der_Exc = (-rE[t] + ReLu( IE + WEE*rE[t] + WEI*rI[t] - gammaE )) /TauE 
  der_Inh = (-rI[t] + ReLu( II + WIE*rE[t] + WII*rI[t] - gammaI ))/TauI
  rE[t+1]= rE[t] + dt * der_Exc
  rI[t+1]= rI[t] + dt * der_Inh

#6. Plotting the above 
plt.figure(figsize=(20,10))
plt.plot(time, rE, label='E population',color='green')
plt.plot(time, rI, label='I population',color='red')
plt.xlabel('time (ms)')
plt.ylabel('rate (Hz)')
plt.legend()
plt.show()

#Phase plane for constant TauI
plt.figure(figsize=(20,10))
plt.plot(rE, rI,color='Cyan')
plt.xlabel('rE (Hz)')
plt.ylabel('rI (Hz)')
plt.title("Phase plane plot (TauI=30)")
plt.show()

#7. Calculation of firing rate of excitatory (we can change if we want) neuron when we
#vary TauI. We plot them  together so the difference in the behaviour is easily visible

#Initialisation of time constant
TauI = np.zeros(10)

#Calculation of firing rate of both neurons populations while varying TauI  
plt.figure(figsize=(20,10))
for i in [30,37,40,41,50]:
  TauI=i
  for t in range(0,steps): #derivative calculation at t point
    der_Exc = (-rE[t]+ ReLu( WEE*rE[t] + WEI*rI[t]  - gammaE )) /TauE 
    der_Inh = (-rI[t] + ReLu( WIE*rE[t]  + WII*rI[t]  - gammaI ))/TauI
    rE[t+1]= rE[t]  + dt * der_Exc
    rI[t+1]= rI[t]  + dt * der_Inh
  
  plt.plot(time, rE, label=f"TauI={TauI}")
    
plt.legend()
plt.xlabel('time (ms)')
plt.ylabel('rate (Hz)')
plt.title("Excitatory neurons population")
plt.show()

#The stability of the fixed point is determined by the real parts of the eigenvalues that
#are given by the following equations. We create a function that calculates them. if
#the real parts of both eigenvalues are less than 0, the fixed point is stable,whereas    
#if either is greater than 0,the fixed point is unstable.If the factor under the radical sign 
#is positive, both eigenvalues are real,and the behavior near the fixed point is exponential  
#This means that there is enponential movement toward the fixed point if both eigenvalues are 
#negative,or away from the fixed point if either eigenvalue is posotive.

def L(x):
  l1=np.array(0.5*((WEE-1)/TauE+(WII-1)/x + cmath.sqrt(((WEE-1)/TauE-(WII-1)/x)**2+4*WEI*WIE/(TauE*x))))
  
  l2=np.array(0.5*((WEE-1)/TauE+(WII-1)/x - cmath.sqrt(((WEE-1)/TauE-(WII-1)/x)**2+4*WEI*WIE/(TauE*x))))
  if l1>0 and l2>0:
      print("stable")
  else:
      print("unstable")
  return l1,l2


#Examples of the above function
y1=L(30)#stable eigenvalues
y2=L(50) #unstable eigenvalues 
