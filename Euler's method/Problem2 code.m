clc;
clear;
k=0.017;
delta_t = 1 ;   %Step Size
end_time=10;
t=0:delta_t:end_time;
Ta=21;
T=68;         % Initialising the temperature to 68 Celcius at t=0
T_previous=68;

for i=1:(length(t)-1)
    T_present=T_previous -k*delta_t*(T_previous-Ta);
    T(end+1)= T_present;
    T_previous=T_present;
end

dT_dt_value= -k*(T-Ta);

fprintf('***************************************************************************************\n')
fprintf('The final Temperature is %1f Celcius \n\n',T(end))
fprintf('***************************************************************************************\n')

% Plot results
figure;
plot(t, T, 'blue');
xlabel('Time (min)');
ylabel('Temperature (Celcius)');
title('Change in Temperature over Time');

Time_min=t';
Temperature_celcius=T';
dT_dt_value=dT_dt_value';
% Combine arrays into a table
result_table = table(Time_min, Temperature_celcius,dT_dt_value);

% Display the table
disp(result_table);
fprintf('**************************************************************************************\n')