#sudo docker run -it --name publisher --network="host" mqtt-publish:v1
docker run -it --rm --name publisher --network="host" mqtt-publish:v1

#nvidia-docker run -it --rm --gpus all --name publisher --network="host" -e PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python mqtt-publish:v1

