nvidia-docker run -it --rm --gpus all --name listener --network="host" ros2-foxy-cuda

$ export ROS_DOMAIN_ID=10
$ ros2 run demo_nodes_py listener

$ ros2 node list
$ ros2 topic list
$ ros2 topic echo /chatter
