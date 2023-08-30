import matplotlib.pyplot as plt
import numpy as np
k=0.1
g=10
step_size=0.25            # Step Size
start_time=0
end_time=10
time=np.arange(start_time,end_time+0.25,step_size)
radius=[3]
for i in range(len(time)-1):
    new_radius=radius[i] - k*step_size
    radius.append(new_radius)
radius=np.array(radius)
volume=(4/3)*(np.pi)*radius**3

avg_evaporation_rate= (radius[-1]-radius[0])/end_time
print("The radius array \n",radius)
print("\nTHe volume array\n",volume)
plt.plot(time,radius)
plt.xlabel("Time in min")
plt.ylabel("Radius in mm")
plt.title("Change in Radius with time")
plt.show()

plt.plot(time,volume,'red')
plt.xlabel("Time in min")
plt.ylabel("Volume in cubic mm")
plt.title("Change in Volume with time")
plt.show()

print("\nThe final radius is " , round(radius[-1],2))
print("The final volume is ", round(volume[-1],2))
print("The average evapotation rate(Change in radius/Total Time) is ", round(avg_evaporation_rate,2))