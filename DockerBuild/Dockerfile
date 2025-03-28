FROM nvidia/cuda:12.2.2-base-ubuntu20.04

# ----------------------------------------------------------------------------
RUN apt-get update
RUN apt-get -y upgrade

# -----------------------------------------------------------------------------
# add locale package & set
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y install locales
RUN locale-gen en_US en_US.UTF-8
RUN update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
RUN export LANG=en_US.UTF-8

# -----------------------------------------------------------------------------
RUN apt-get install -y software-properties-common
RUN add-apt-repository universe

RUN apt-get install -y curl  


# Add ROS 2 apt repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | apt-key add - && \
    add-apt-repository universe && \
    echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list

RUN apt-get update
RUN apt-get -y upgrade 

RUN apt-get install -y ros-foxy-desktop 
RUN apt-get install -y python3-argcomplete
RUN apt-get install -y ros-dev-tools

#RUN apt-get install -y ros-foxy-joint-state-publisher-gui 
#RUN apt-get install -y ros-foxy-xacro 
RUN apt-get install -y python3-colcon-common-extensions 
RUN apt-get install -y python3-vcstool

# Source ROS 2 on every shell start
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc

##### INSTALL CycloneDDS to communicate between docker container in same host
RUN apt-get install -y ros-foxy-rmw-cyclonedds-cpp
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

ENV ROS_DOMAIN_ID 10

# Install demo talker/listener packages (C++ and Python)
RUN apt-get update && apt-get install -y \
    ros-foxy-demo-nodes-cpp \
    ros-foxy-demo-nodes-py \
    && rm -rf /var/lib/apt/lists/*

# Default to bash
CMD ["/bin/bash"]
