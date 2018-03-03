Quick&dirty poc to do face detection on the edge. this is based on the [work of Ville Rantala](https://github.com/vjrantal/iot-edge-darknet-module)

to make it work:

1. Clone Ville's [git](https://github.com/vjrantal/iot-edge-darknet-module) 
2. change the base image to point to FROM UBUNTU:17.10
2. build the docker image vjrantal/azure-iot-sdk-python
3. clone and build the [Iot sdk for Python](https://github.com/Azure/azure-iot-sdk-python) on your system 
4. copy the file iothub_client.so to the root of this solution
5. docker build the image and push it to a repo.
6. deploy it to the edge with the option : 

{"HostConfig":
{
"Privileged": true
}
}
