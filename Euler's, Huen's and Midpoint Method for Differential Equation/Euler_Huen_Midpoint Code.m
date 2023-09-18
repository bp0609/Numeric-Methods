% Parameters
a = 1.2;
b = 0.6;
c = 0.8;
d = 0.3;
h = 0.1;       %Step Size (dt)
T = 20;

% Initial conditions
x0 = 2;
y0 = 1;

% Number of time steps
num_steps = (T/h) + 1;

% Initialize arrays to store results
x_euler = zeros(num_steps, 1);
y_euler = zeros(num_steps, 1);
x_heun = zeros(num_steps, 1);
y_heun = zeros(num_steps, 1);
x_midpoint = zeros(num_steps, 1);
y_midpoint = zeros(num_steps, 1);

% Initialize initial conditions
x_euler(1) = x0;
y_euler(1) = y0;
x_heun(1) = x0;
y_heun(1) = y0;
x_midpoint(1) = x0;
y_midpoint(1) = y0;

% Simulate using Euler's method, Heun's method, and Midpoint method
for i = 2:num_steps
    % Euler's method
    dx_euler = h * (a * x_euler(i - 1) - b * x_euler(i - 1) * y_euler(i - 1));
    dy_euler = h * (-c * y_euler(i - 1) + d * x_euler(i - 1) * y_euler(i - 1));
    x_euler(i) = x_euler(i - 1) + dx_euler;
    y_euler(i) = y_euler(i - 1) + dy_euler;
    
    % Predict using Heun's method
    x_pred = x_heun(i - 1) + h * (a * x_heun(i - 1) - b * x_heun(i - 1) * y_heun(i - 1));
    y_pred = y_heun(i - 1) + h * (-c * y_heun(i - 1) + d * x_heun(i - 1) * y_heun(i - 1));
    dx_pred = h * (a * x_pred - b * x_pred * y_pred);
    dy_pred = h * (-c * y_pred + d * x_pred * y_pred);
    
    % Correct using Heun's method
    x_heun(i) = x_heun(i - 1) + 0.5 * (dx_euler + dx_pred);
    y_heun(i) = y_heun(i - 1) + 0.5 * (dy_euler + dy_pred);
    
    % Midpoint method
    dx_midpoint = h * (a * x_midpoint(i - 1) - b * x_midpoint(i - 1) * y_midpoint(i - 1));
    dy_midpoint = h * (-c * y_midpoint(i - 1) + d * x_midpoint(i - 1) * y_midpoint(i - 1));
    x_midpoint(i) = x_midpoint(i - 1) + 0.5 * dx_midpoint;
    y_midpoint(i) = y_midpoint(i - 1) + 0.5 * dy_midpoint;
end

% Time values
t = 0:h:T;

% Plot the results
figure;
subplot(1, 2, 1);
plot(t, x_euler, 'b-', t, x_heun, 'g-', t, x_midpoint, 'r-');
xlabel('Time');
ylabel('Prey (x)');
legend("Euler's Method", "Heun's Method", "Midpoint Method");

subplot(1, 2, 2);
plot(t, y_euler, 'b-', t, y_heun, 'g-', t, y_midpoint, 'r-');
xlabel('Time');
ylabel('Predator (y)');
legend("Euler's Method", "Heun's Method", "Midpoint Method");

sgtitle('Lotka-Volterra Predator-Prey Model Simulations');