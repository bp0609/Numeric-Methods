import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Empirical Constants
a=12.02
b=0.08407

T=400               #Temperature in kelvin 
p=2.5               #Pressure in atm
R=0.082057338       #Real gas constant in L.atm.K-1.mol-1

xl_lst=[]
xu_lst=[]
xr_lst=[]
ea_lst=[]

#V is molar volume in L.atm-1.
# Defining a function of V that returns the value of Van der Waals equation
def f(V):
    return (p+(a/(V**2)))*(V-b) - R*T

def falsePosition(xl,xu,es,imax):
    iter=0
    fl=f(xl)
    fu=f(xu)
    xr=False
    while (True):
        if iter==0:
            xr_old= xl- ((fl*(xu-xl))/(fu-fl))
        else:
            xr_old= xr
        xr= xl- ((fl*(xu-xl))/(fu-fl))
        iter= iter +1
        if xr!=0:
            ea=np.abs((xr-xr_old)/xr)*100
    #appending to list
        xl_lst.append(xl)        
        xr_lst.append(xr)        
        xu_lst.append(xu)        
        ea_lst.append(ea)        
        
        test= fl*f(xr)
        if test<0:
            xu=xr
            fu=f(xu)
        elif test>0:
            xl=xr
            fl=f(xl)
        else:
            ea=0
        if (ea<es or iter>=imax) and iter>1:
            return xr,ea,iter
            
es=0.005
iter_max=100
root,ea,iter=falsePosition(1,20,es,iter_max)
print("*"*100)
print("The value of 'V' found by False position method is ",root)
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
print("*"*100)

V_lst=list(np.arange(0.1,20,0.001))
f_lst=[]
for i in V_lst:
    f_lst.append(f(i)) 
plt.plot(V_lst,f_lst)
plt.xlabel("Molar Volume V")
plt.ylabel("f(V)")
plt.title("Graph of f(V) v/s V")
plt.grid(True)
plt.show()