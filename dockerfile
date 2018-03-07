FROM vjrantal/azure-iot-sdk-python 
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-scipy
RUN apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get update
WORKDIR /azure-iot-sdk-python/device/samples
run pip3 install picamera 
run pip3 install face_recognition
RUN apt-get install libraspberrypi-bin -y
RUN usermod -a -G video root
COPY *.py ./
COPY img/* img/
ENTRYPOINT ["python3","main.py"]