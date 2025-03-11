# MQTT Broker(Mosquitto) 환경설정
## Mosquitto 설치
```sh
$ sudo apt-get update && sudo apt-get upgrage
$ sudo apt-get install mosquitto
$ sudo apt-get install mosquitto-clients # 생략 가능
```

## Mosquitto 구동
```sh
$ sudo /etc/init.d/mosquitto <start|stop|restart|reload|force-reload|status>
```

# Docker 설치
## Docker CE(Community Edition) 설치를 추천
```sh
$ apt-get update
$ sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```
## Docker compose plugin 설치
```sh
$ sudo apt-get install docker-compose-plugin
```

## Add user to docker group
```sh
$ sudo groupadd -f docker
$ sudo usermod -aG docker <UserName>
```
## Nvidia Container Toolkit 설정
### Stable repository 및 GPG key 설정
```sh
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```
### install nvidia-docker
```sh
sudo apt-get update
sudo apt-get install -y nvidia-docker2
```

### restart docker daemon
```sh
sudo systemctl restart docker
```

### base CUDA container 테스트
```sh
sudo nvidia-docker run --rm --gpus all nvidia/cuda:12.2.2-base-ubuntu20.04 nvidia-smi
```

# Docker Image Build
## Publisher build
```sh
$ cd Publisher
```

```sh
$ cat Dockerfile
```
```
FROM python:3.8

RUN pip3 install paho-mqtt
COPY publish.py publish.py

CMD python3 publish.py
```

```sh
$ docker build -t mqtt-publish:v1 .
```

```sh
$ docker images
```

### nvidia-docker 예제
```sh
$ cat Dockerfile-nvidia
```
```
FROM nvidia/cuda:12.2.2-base-ubuntu20.04
#FROM python:3.8

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt install python3.8 -y
RUN apt install python3-pip -y

RUN pip3 install paho-mqtt
RUN pip3 install etcd3

COPY publish.py publish.py

CMD python3 publish.py

```

### Subscriber build
```sh
$ cd Subscriber
```

```sh
$ cat Dockerfile
```

```
FROM python:3.8

RUN pip3 install paho-mqtt
COPY publish.py publish.py

CMD python3 publish.py
```

```sh
$ docker build -t mqtt-subscribe:v1 .
```

```sh
$ docker images
```

# Run with docker compose

```sh
$ cd PubSub
```

```sh
$ cat docker-compose.yml
```
```
version: '3.8'
services:
  mqtt-subscribe:
    image: "mqtt-subscribe:v1"
    container_name: mqtt-sub
    network_mode: "host"
    tty: true
    environment: 
       PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION: python
#    volumes:
#       - ./data:/data
  mqtt-publish:
    image: "mqtt-publish:v1"
    container_name: mqtt-pub
    network_mode: "host"
    tty: true
    environment: 
       PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION: python
#    volumes:
#       - aimd_nas_volume:/data

#volumes:
#  aimd_nas_volume:
#    driver: local
#    driver_opts:
#      type: "nfs"
#      o: "addr=<NAS_IP>, rw"
#      device: ":/nas_shared_folder"

```


``` sh
$ docker compose up
```
