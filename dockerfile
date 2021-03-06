FROM mandrx/azure-iot-sdk-python-arm
RUN apt-get -y install python3-pip
RUN apt-get -y install python3-scipy
RUN apt-get -y install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get update
WORKDIR /azure-iot-sdk-python/device/samples
run pip3 install picamera 
run pip3 install face_recognition
run apt-get -y install software-properties-common python-software-properties
run add-apt-repository ppa:ubuntu-raspi2/ppa
RUN apt-get update
RUN apt-get  -y install libraspberrypi-bin
COPY *.py ./
COPY img/* img/
ENTRYPOINT ["python3","-u","main.py"]