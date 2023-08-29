import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

k1=50000
k2=40
m=90
g=9.81
h=0.45
d=0

xl_lst=[]
xu_lst=[]
xr_lst=[]
ea_lst=[]
et_lst=[]

def f(d):
    return (2*k2)*(d**(5/2))/5 + k1*(d**2)/2 -m*g*d - m*g*h

def bisect(xl,xu,es,imax):
    iter=0
    xr=False
    while (True):
        if iter==0:
            xr_old= (xl+xu)/2
        else:
            xr_old= xr
        xr=(xl+xu)/2
        iter= iter +1
        if xr!=0:
            ea=np.abs((xr-xr_old)/xr)*100
    #appending to list
        xl_lst.append(xl)        
        xr_lst.append(xr)        
        xu_lst.append(xu)        
        ea_lst.append(ea)        
        
        test= f(xl)*f(xr)
        if test<0:
            xu=xr
        elif test>0:
            xl=xr
        else:
            ea=0
        if (ea<es or iter>=imax) and iter>1:
            return xr,ea,iter
            
es=0.05
iter_max=100
root,ea,iter=bisect(0,0.2,es,iter_max)

print("\nThe value of 'd' found by bisection algorithm is ",root)
print("\nThe number of iterations required to get to the answer were ", iter)
print("\nThe stopping criteria 'es' used was ", es,"%")
print("\nThe value of 'ea' is ",ea, "%\n")

print("*"*100)
ea_lst[0]='-'
dict={"Iteration":np.arange(1,iter+1,1),
    "x_l":xl_lst,
    "x_u":xu_lst,
    "x_r":xr_lst,
    "ea(%)":ea_lst,}
df=pd.DataFrame(dict)

print(df)


########################################
d_lst=list(np.arange(0.001,0.2,0.001))
f_lst=[]
for i in d_lst:
    f_lst.append(f(i)) 
plt.plot(d_lst,f_lst)
plt.xlabel("f(d)")
plt.ylabel("d")
plt.title("Graph of f(d) v/s d")
plt.grid(True)

plt.show()
