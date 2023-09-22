import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Constants
g = 9.81  # gravitational constant (m/s^2)
cd = 0.25  # second-order drag coefficient (kg/m)
m = 68.1  # mass (kg)
k = 40  # cord spring constant (N/m)
gamma = 8  # cord dampening coefficient (Ns/m)
L = 30  # cord length (m)
t_max = 50  # maximum time (s)
dt = 0.01  # time step (s)
initial_x = 0  # initial position (m)
initial_v = 0  # initial velocity (m/s)

# Initialize arrays to store results
t_values = np.arange(0, t_max + dt, dt)
x_values = np.zeros_like(t_values)
v_values = np.zeros_like(t_values)

# Define the differential equation
def f(t, x, v):
    if x <= L:
        return g - np.sign(v) * (cd / m) * v**2
    else:
        return g - np.sign(v) * (cd / m) * v**2 - (k / m) * (x - L) - (gamma / m) * v

# Perform Fourth-order Runge-Kutta integration
for i in range(len(t_values) - 1):
    t = t_values[i]
    x = x_values[i]
    v = v_values[i]

    k1v = dt * f(t, x, v)
    k1x = dt * v
    k2v = dt * f(t + dt/2, x + k1x/2, v + k1v/2)
    k2x = dt * (v + k1v/2)
    k3v = dt * f(t + dt/2, x + k2x/2, v + k2v/2)
    k3x = dt * (v + k2v/2)
    k4v = dt * f(t + dt, x + k3x, v + k3v)
    k4x = dt * (v + k3v)

    x_values[i+1] = x + (k1x + 2*k2x + 2*k3x + k4x) / 6
    v_values[i+1] = v + (k1v + 2*k2v + 2*k3v + k4v) / 6

dict={
    'Time(sec)': t_values,
    'Position(x)': x_values,
    'Velocity(v)': v_values,
          }
df=pd.DataFrame(dict)
print(df)

# To see all the values comment out the below to lines
# for i in range(len(t_values)):
#     print(f"t = {t_values[i]:.2f} s, x = {x_values[i]:.2f} m, v = {v_values[i]:.2f} m/s")


# Plot the graph
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(t_values, x_values, label='Position (m)')
plt.title('Bungee Jumper Position vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t_values, v_values, label='Velocity (m/s)', color='orange')
plt.title('Bungee Jumper Velocity vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)

plt.tight_layout()
plt.show()


# --------------------------------------------------------------------------------------------------------------
