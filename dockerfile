FROM vjrantal/azure-iot-sdk-python 
RUN apt-get update && \
        apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libpq-dev \
        libgtk2.0-dev \
         pkg-config
RUN pip3 install numpy
WORKDIR /azure-iot-sdk-python/device/samples
run pip3 install face_recognition
COPY *.py ./
COPY img/* img/
ENTRYPOINT ["python3","main.py"]