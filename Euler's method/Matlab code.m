clc;
clear;
k=0.1;
delta_t = 0.25;   %Step Size
end_time=10;
t=0:delta_t:end_time;
radius=3;         % Initialising the radius to 3 mm at t=0
r_previous=3;

for i=1:(length(t)-1)
    r_present=r_previous -k*delta_t;
    radius(end+1)= r_present;
    r_previous=r_present;
end

avg_evaporation_rate= (radius(end)-radius(1))/end_time;

volume= (4*pi*radius.^3)/3;
dv_dt_values = -k*(4*pi*radius.^2);
%plot(t,radius);

fprintf('The final radius is %1f mm \n',radius(end))
fprintf('The final volume is %1f cubic mm \n',volume(end))
fprintf('The average evapotation rate(Change in radius/Total Time) is %2f mm/min \n',avg_evaporation_rate)

% Plot results
figure;
subplot(2, 1, 1);
plot(t, radius, 'blue');
xlabel('Time (min)');
ylabel('Radius (mm)');
title('Change in Radius over Time');

subplot(2, 1, 2);
plot(t, volume, 'red');
xlabel('Time (min)');
ylabel('Volume (mm^3)');
title('Change in Volume over Time');

time=t';
radius=radius';
volume=volume';
dv_dt_values=dv_dt_values';
% Combine arrays into a table
result_table = table(time, radius, volume, dv_dt_values);

% Display the table
disp(result_table);

