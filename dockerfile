FROM vjrantal/azure-iot-sdk-python 
RUN apt-get update && \
        apt-get install -y \
        python3-picamera
WORKDIR /azure-iot-sdk-python/device/samples
run pip3 install face_recognition
COPY *.py ./
COPY img/* img/
ENTRYPOINT ["python3","main.py"]