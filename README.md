# Mosquitto 환경설정
## Mosquitto 설치
## Mosquitto 구동


# Docker Image Build
## Publisher
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

### Subscriber
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
#    volumes: 
#       - ./data:/data
  mqtt-publish:
    image: "mqtt-publish:v1"
    container_name: mqtt-pub
    network_mode: "host"
    tty: true
```

``` sh
$ docker compose up
```
