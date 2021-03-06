'''
Author: Zihao Wang
This is continuum model for homobilayer TMD MoTe2
Bands calculation using plane wave expansion
'''

import numpy as np 
import matplotlib.pyplot as plt 
from numpy import pi, sin, cos, exp, sqrt 
#define constant
theta = 4.0     #degree
V     = 7.9     #meV
psi   = 142.0   #degree
w     = 18.0    #meV
Vz    = -34.3    #displacement field, meV
#meff  = 0.661157    #electron mass
a0    = 3.297   #angstrom
N     = 6       #truncate range
I     = complex(0, 1)
valley = -1
#tune parameter
def Rot(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], \
        [np.sin(theta), np.cos(theta)]])

theta = theta * pi / 180.0
V = V * 10**(-3)
w = w * 10**(-3)
Vz = Vz * 10**(-3)
psi = psi * pi / 180.0
#hbar = 4.135667 * 10**(-15)/2/pi
#me = 0.51099895 * 10**(6)
#m_eff = meff*me
#kin = -hbar**2/2/m_eff *9*10**(16)
a0 = a0 * 10**(-10)
meff = 1.6/2/(1.1*a0)**2
kin = -1/2/meff
a1 = a0 * np.array([1, 0])
a2 = Rot(pi/3).dot(a1)
G1 = 4*pi/sqrt(3)/a0*np.array([0, 1])
g1 = theta*np.array([G1[1], -G1[0]])
g2 = theta*np.array([G2[1], -G2[0]])
kD = g1[0]/sqrt(3)
Kb = np.array([-vallley*kD*sqrt(3)/2, -valley*kD/2])
Kt = np.array([-valley*kD*sqrt(3)/2, valley*kD/2])

#define Lattice
L = []
invL = np.zeros((2*N+1, 2*N+1), int)
def Lattice(n):
    count = 0
    #bottom
    for i in np.arange(-n, n+1):
        for j in np.arange(-n, n+1):
            L.append([i, j])
            invL[i+n, j+n] = count
            count = count + 1
    #top
    for i in np.arange(-n, n+1):
        for j in np.arange(-n, n+1):
            L.append([i, j])

Lattice(N)
siteN = (2*N+1)**2
L = np.array(L)

def SolvHamiltonian(kx, ky):
    H = np.zeros((2*siteN, 2*siteN), dtype=complex)
    for i in np.arange(siteN):
        ix = L[i, 0]
        iy = L[i, 1]

        ax = kx - Kb[0] + ix*g1[0] + iy*g2[0]
        ay = ky - Kb[1] + ix*g1[1] + iy*g2[1]
        H[i, i] += kin * (ax**2 + ay**2) + Vz/2

        ax = kx - Kt[0] + ix*g1[0] + iy*g2[0]
        ay = ky - Kt[1] + ix*g1[1] + iy*g2[1]
        H[i+siteN, i+siteN] += kin * (ax**2 + ay**2) - Vz/2

        H[i+siteN, i] += w
        H[i, i+siteN] += w


        if (ix != N):
            j = invL[ix+1 +N, iy +N]
            H[j, i] += V*exp(I*psi)
            H[j+siteN, i+siteN] += V*exp(-I*psi)
        if (iy != -N):
            j = invL[ix +N, iy-1 +N]
            H[j, i] += V*exp(I*psi)
            H[j+siteN, i+siteN] += V*exp(-I*psi)
            if (valley == +1):
                H[j, i+siteN] += w
            elif (valley == -1):
                H[j+siteN, i] += w
        
        if ((ix != -N) and (iy != N)):
            j = invL[ix-1 +N, iy+1 +N] 
            H[j, i] += V*exp(I*psi)
            H[j+siteN, i+siteN] += V*exp(-I*psi)
            if (valley == +1):
                H[j+siteN, i] += w
            elif (valley == -1):
                H[j, i+siteN] += w
            

        if (ix != -N):
            j = invL[ix-1 +N, iy +N]
            H[j, i] += V*exp(-I*psi)
            H[j+siteN, i+siteN] += V*exp(I*psi)
        if (iy != N):
            j = invL[ix +N, iy+1 +N]
            H[j, i] += V*exp(-I*psi)
            H[j+siteN, i+siteN] += V*exp(I*psi)
            if (valley == +1):
                H[j+siteN, i] += w
            elif (valley == -1):
                H[j, i+siteN] += w
            
        if ((ix != N) and (iy != -N)):
            j = invL[ix+1 +N, iy-1 +N] 
            H[j, i] += V*exp(-I*psi)
            H[j+siteN, i+siteN] += V*exp(I*psi)
            if (valley == +1):
                H[j, i+siteN] += w
            elif (valley == -1):
                H[j+siteN, i] += w

    eigenE = np.linalg.eigvalsh(H)
    return eigenE

Num = 50
#+K vallley
KX = list(np.linspace(0,-g1[0]/2,Num)) + list(np.linspace(-g1[0]/2,-g1[0]/2,Num)) 
KY = list(np.linspace(0,-g1[0]/np.sqrt(3)/2,Num)) + list(np.linspace(-g1[0]/np.sqrt(3)/2,g1[0]/np.sqrt(3)/2,Num))
#-K valley
# KX = list(np.linspace(0,-g1[0]/2,Num)) + list(np.linspace(-g1[0]/2,-g1[0]/2,Num)) 
# KY = list(np.linspace(0,g1[0]/np.sqrt(3)/2,Num)) + list(np.linspace(g1[0]/np.sqrt(3)/2,-g1[0]/np.sqrt(3)/2,Num))

Eigen = np.zeros((len(KX),2*siteN))
for k in range(len(KX)):
    Eigen[k,:] = SolvHamiltonian(KX[k], KY[k])
plt.plot(np.linspace(0,1,len(KX)),Eigen*1000,'b-')
plt.hlines(0, 0, 1, colors='k')
plt.vlines(0.5, -100, 100, colors='k', linestyles='--')
plt.ylim(-50,30)
plt.xlim(0,1)
plt.ylabel('E(meV)')

plt.show()
