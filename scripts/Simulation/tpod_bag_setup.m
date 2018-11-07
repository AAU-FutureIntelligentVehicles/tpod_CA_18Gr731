clear all

%takes the specified bag file
bag = rosbag('test.bag');       

%Isolates specific topic from selected rosbag
right_bag = bag.select( 'Topic', '/ticks_right');  
left_bag = bag.select( 'Topic', '/ticks_left');             
gps_bag = bag.select( 'Topic', '/raw_gps');

% Read the messages from specified bags
leftdata = readMessages(left_bag);
rightdata = readMessages(right_bag);
gpsmessage = readMessages(gps_bag);

% Preallocation for faster calculcations in the loop
gps_strings = strings(gps_bag.NumMessages, 1);
angle_strings = strings(gps_bag.NumMessages, 1);
%angle = zeros(gps_bag.NumMessages, 1);
rightencoder = zeros(right_bag.NumMessages, 1);
leftencoder = zeros(left_bag.NumMessages, 1);

j = 1; % Counter for GPGGA messages
k = 1; % Counter for angle messages

for i=2:gps_bag.NumMessages                                         % The first message from gps is always a false GPGGA data
    if gpsmessage{i}.Data(2:6) == "GPGGA"                           % Find GPGGA messages
        gps_strings(j) = gpsmessage{i}.Data; 
        charline = char(gps_strings(j));                            % string2char
        long(j) = str2double(string(charline(18:29)));              % Get longitudinar datas
        lat(j) = str2double(string(charline(33:45)));               % Get latitude datas
        j = j + 1;
        
    elseif gpsmessage{i}.Data(2:5) == "PTNL"                        % Find angle messages
        angle_strings(k) = gpsmessage{i}.Data;
        start = strfind(angle_strings(k),'0,+');                    % Starting point of angle data
        ending = strfind(angle_strings(k),',Yaw');                  % Ending point of angle data
        charline = char(angle_strings(k));                          % string2char
        angle(k) = str2double(string(charline((start+3):ending)));
        if angle(k) == 0                                            % If we lost data our angle became exatly zero
            angle(k) = angle(k-1);
        end
        k = k + 1;
    end
end

%Get right encoder datas to array (without time)
for i=1:right_bag.NumMessages
     rightencoder(i) = [rightdata{i}.Data];
end

%Get left encoder datas to array (without time)
for i=1:left_bag.NumMessages
     leftencoder(i) = [leftdata{i}.Data];
end

% Encoder datas with timeseries
left_timeseries = bagleft.timeseries;
tsleft = setuniformtime(left_timeseries, 'starttime', 0, 'endtime', bagleft.EndTime - bagleft.StartTime);
right_timeseries = bagright.timeseries;
tsright = setuniformtime(right_timeseries, 'starttime', 0, 'endtime', bagright.EndTime - bagright.StartTime);

% Plot GPS and angle datas
figure(1);
plot(lat, long) %plot the route
title("route by GPS data");

figure(2);
plot(angle)
title("angle datas");

