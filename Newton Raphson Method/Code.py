import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Empirical Constants
L=600
E=50000
I=30000
w=2.5


xr_lst=[]
ea_lst=[]

#V is molar volume in L.atm-1.
# Defining a function of V that returns the value of Van der Waals equation
def df_dx(x):
    return (w/(120*E*I*L))*(-20*(x**3)+12*(L**2)*x)
def f(x):
    return (w/(120*E*I*L))*(-5*(x**4)+6*(L**2)*(x**2)-(L**4))
def g(x):
    return (w/(120*E*I*L))*(-1*(x**5)+2*(L**2)*(x**3)-(L**4)*x)


def newtonRaphson(x0,es,imax):
    iter=0
    xr=x0
    xr_lst.append(xr)
    while (iter<imax):
        xr_old= xr
        xr= xr- (f(xr)/df_dx(xr)) 
        iter= iter +1
        if xr!=0:
            ea=np.abs((xr-xr_old)/xr)*100
    #appending to list
        xr_lst.append(xr)               
        ea_lst.append(ea)        
        
        if ea<es  and iter>1:
            return xr,ea,iter
    return "Convergence not achieved"
            
es=0.0005
iter_max=100
ea_lst.append("-")
root,ea,iter=newtonRaphson(200,es,iter_max)
print("*"*100)
print("The point of maximum deflection is ",root, " cm")
print("\nThe magnitude of maximum deflection is ",g(root)," cm")
print("\nThe number of iterations required to get to the answer were ", iter)
print("\nThe stopping criteria 'es' used was ", es,"%")
print("\nThe value of 'ea' is ",ea, "%\n")

print("*"*100)

et_lst=[]
for i in xr_lst:
    et=np.abs((xr_lst[-1]-i)/xr_lst[-1])*100   
    et_lst.append(et)
dict={"Iteration":np.arange(1,iter+2,1),
    "x_i+1":xr_lst,
    "ea(%)":ea_lst,
    "et(%)":et_lst,}

df=pd.DataFrame(dict)
print(df)
print("*"*100)
x_lst=list(np.arange(0,700,0.001))
f_lst=[]
for i in x_lst:
    f_lst.append(f(i)) 
plt.plot(x_lst,f_lst)
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Graph of f(x) v/s x")
plt.grid(True)
plt.show()
