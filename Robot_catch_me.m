function [theta2 ,phi2 ,lamda2 ] = Robot_catch_me(xn,yn,theta1,phi1,lamda1)
xn=double(xn);
yn=double(yn);
theta1=double(theta1);
phi1=double(phi1);
lamda1=double(lamda1);
ln = sqrt(xn^2+yn^2); %mm
gamma = atan(yn/xn); %rad
l1 = 10;
l2 = 10;
l3 = 4;
x1 = l1*cos(theta1);
x2 = l2*cos(phi1)+x1;
x3 = l3*cos(lamda1)+x2;
y1 = l1*sin(theta1);
y2 = l2*sin(phi1)+y1;
y3 = l3*sin(lamda1)+y2;

x_target=xn;
y_target=yn;


x = 0:0.1:l1 ;
y = sqrt(l1^2 - x.^2);
y =  [y -flip(y)];
x = [x flip(x)];

%Constraints
y_c = -3;

for i = length(x):-1:1
    if y(i) <y_c
        y(i) = [];
        x(i) = [];
    end
end

radius=(x_target^2+y_target^2)^0.5;
phi=atan(y_target/x_target);
radius2=((x_target-x(1))^2+(y_target-y(1))^2)^0.5;
radius3=((x_target-x(end))^2+(y_target-y(end))^2)^0.5;
% radius
% radius2
% radius3
% radius<(l1+l2)
% radius>l1
% radius3>l2
% radius2>l2
if (radius<(l1+l2)) && (radius>l1) % && ((radius3>l2) && (radius2>l2))
    flag=1;
else
    disp('non feasible position')
    flag=0;

end

%Assumption;
if flag
lamda2 = 0;
%Equation system
syms theta2 phi2 x12 x22 y12 y22 

x32 = xn;
y32 = yn;

eq1 = x12 == l1*cos(theta2);
eq2 = x22 == l2*cos(phi2)+x12;
eq3 = x32 == l3*cos(lamda2)+x22;
eq4 = y12 == l1*sin(theta2);
eq5 = y22 == l2*sin(phi2)+y12;
eq6 = y32 == l3*sin(lamda2)+y22;
 
eqn = [eq1,eq2,eq3,eq4,eq5,eq6];

[theta2,phi2,x12,x22,y12,y22] = solve(eqn,[theta2,phi2,x12,x22,y12,y22],'Real',true);

plot([0 x12(1)],[0 y12(1)],'g')
hold on
plot([x12(1) x22(1)],[y12(1) y22(1)],'m')
hold on
plot([x22(1) x32(1)],[y22(1) y32(1)],'b')
plot(xn,yn,'o')
hold on
plot([0 x12(2)],[0 y12(2)],'g')
hold on
plot([x12(2) x22(2)],[y12(2) y22(2)],'m')
hold on
plot([x22(2) x32],[y22(2) y32],'b')

theta2= rad2deg(double(theta2(2)));
phi2= rad2deg(double(phi2(2)));


% syms x y real
% x = 0:0.1:l1 ;
% y = sqrt(l1^2 - x.^2);
% y =  [y -flip(y)];
% x = [x flip(x)];

% %Constraints
% y_c = -3;
% 
% for i = length(x):-1:1
%     if y(i) <y_c
%         y(i) = [];
%         x(i) = [];
%     end
% end
% plot(x,y)
% hold on
% axis equal
% 
% % 
%  phi_max = pi/2;
%  phi_min = -pi/5;
%  angles = phi_min : pi/14 : phi_max;
% for i = 1 : length(x)
%     for j = 1:length(angles)
%         x_l2(i,j) = x(i)+l2*cos(angles(j));
%         y_l2(i,j) = y(i) +l2*sin(angles(j)); 
%         
%     end
% 
%     
%     %plot(x_l2(i,:),y_l2(i,:))
%     %hold on
%    % pause(0.5)
% end
% plot(x_l2(1,:),y_l2(1,:))
% plot(x_l2(end,:),y_l2(end,:))
% 
% for j = 1:length(angles)
%         x_l(j) = (l1+l2)*cos(angles(j));
%         y_l(j) =  (l1+l2)*sin(angles(j)); 
%         
% end
%     plot(x_l,y_l)

% x(1)
% y(1)

else 
    theta2=5000;
phi2=5000;
lamda2=5000;
end
%CHECK for FEASIBILITY
% for i=1:1:400
% x_target=30 .* rand(1,1);
% y_target=-14+20 .* rand(1,1);
% 
% radius=(x_target^2+y_target^2)^0.5;
% phi=atan(y_target/x_target);
% radius2=((x_target-x(1))^2+(y_target-y(1))^2)^0.5;
% radius3=((x_target-x(end))^2+(y_target-y(end))^2)^0.5;
% if (radius<(l1+l2)) && (radius>l1)% && ((radius3>l2) && (radius2>l2))
%     plot(x_target,y_target,'o','MarkerEdgeColor','g')
% else
%     plot(x_target,y_target,'o','MarkerEdgeColor','r')
% end
% hold on





end






