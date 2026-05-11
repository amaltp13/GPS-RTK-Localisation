#!/bin/bash

SESSION="rtk"

# Kill old session if exists
tmux kill-session -t $SESSION 2>/dev/null

# Create new session
tmux new-session -d -s $SESSION

# Pane 1: GPS Bridge
tmux send-keys -t $SESSION "
source /opt/ros/humble/setup.bash;
source ~/ros2_ws/install/setup.bash;
echo 'GPS Bridge';
ros2 run gps_rtk_pkg gps_bridge
" C-m

# Split horizontally → Pane 2 (NTRIP)
tmux split-window -h
tmux send-keys "
source /opt/ros/humble/setup.bash;
source ~/ros2_ws/install/setup.bash;
echo 'NTRIP Client';
ros2 launch ntrip_client ntrip_client_launch.py \
    host:=54.206.56.130 \
    port:=2101 \
    mountpoint:(your mount point)\
    username:=(username_from_rtkdata)\
    password:=*your_password)\
    authenticate:=true \
    nmea_topic:=/nmea
" C-m

# Select pane 0 again
tmux select-pane -t 0

# Split vertically → Pane 3 (GPS Fix)
tmux split-window -v
tmux send-keys "
source /opt/ros/humble/setup.bash;
source ~/ros2_ws/install/setup.bash;
echo 'GPS Fix';
ros2 run gps_rtk_pkg gps_fix_node
" C-m

# Move to right pane
tmux select-pane -t 1

# Split vertically → Pane 4 (GPS XY)
tmux split-window -v
tmux send-keys "
source /opt/ros/humble/setup.bash;
source ~/ros2_ws/install/setup.bash;
echo 'GPS XY';
ros2 run gps_rtk_pkg gps_xy_node
" C-m

# Bottom full-width pane → RTK status
tmux new-window -t $SESSION -n "RTK Status"
tmux send-keys "
source /opt/ros/humble/setup.bash;
source ~/ros2_ws/install/setup.bash;
echo 'RTK Status (GGA)';
while true; do
  ros2 topic echo /nmea --once | grep GNGGA;
  sleep 1;
done
" C-m

# Attach session
tmux attach -t $SESSION
