import numpy as np
import pandas as pd

k1=10
k2=30
k3=30
k4=10
m1=2
m2=2
m3=2
a1=-0.4
a2=0
a3=0

A=[[-(k1+k2)/m1,k2/m1,0],[k2,-(k2+k3),k3],[0,k3,-(k3+k4)]]  #TDM matrix A 
b=[a1,a2,a3]  
print("TDMA Matrix \n",np.array(A),"\n")


n=3   
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
x=[0]*n
x[n-1]=d[n-1]/f[n-1]
for k in range(n-2,-1,-1):
    x[k]=(d[k]-g[k]*x[k+1])/f[k]


print("The value of x1 is ", x[0],"m")
print("The value of x2 is ", x[1],"m")
print("The value of x3 is ", x[2],"m")