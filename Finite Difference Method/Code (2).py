import numpy as np
import matplotlib.pyplot as plt

# Parameters
D = 1.5e-6  # cm^2/s
k = 5e-6    # s^(-1)
L = 4.0     # cm
A_initial = 0.1  # M
A_final = 0.0    # M

# Discretization
N = 400  # Number of points
h = L / N
x = np.linspace(0, L, N+1)


A = [0]*(N-1)
A[0] = [-(2*D+k*(h**2)),D]+[0]*(N-3)
A[-1]=[0]*(N-3)+[D,-(2*D+k*(h**2))]
for i in range(N-3):
    A[i+1]=[0]*(i) + [D,-(2*D+k*(h**2)),D]+ [0]*(N-i-4)

b=[-A_initial*D]+[0]*(N-3)+[0]


n=N-1   
g=[]
f=[]
e=[]
for i in range(n):
    f=f+[A[i][i]]
    e.append(A[i][i-1]) if i>0 else e.append('-')
    g.append(A[i][i+1]) if i<n-1 else g.append('-')
    

#Decomposition of Tridiagonal Matrix
for k in range(1,n):
    e[k]=e[k]/f[k-1]
    f[k]=f[k]-(e[k]*g[k-1])

# Forward Substitution
d=[0]*n
d[0]=b[0]
for i in range(1,n):
    d[i]=b[i]-(e[i]*d[i-1])

# Backward substitution
Conc_A=[0]*n
Conc_A[n-1]=d[n-1]/f[n-1]
for k in range(n-2,-1,-1):
    Conc_A[k]=(d[k]-g[k]*Conc_A[k+1])/f[k]


Conc_A=[A_initial]+Conc_A+[A_final]


# Plot the concentration profile
plt.figure(figsize=(8, 6))
plt.plot(x, Conc_A, linestyle='-')
plt.xlabel('Distance (cm)')
plt.ylabel('Concentration of A (M)')
plt.title('Concentration Profile of A in the Tube')

plt.grid(True)
plt.show()
