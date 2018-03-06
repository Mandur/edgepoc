FROM vjrantal/azure-iot-sdk-python 
RUN apt-get update && \
     
WORKDIR /azure-iot-sdk-python/device/samples
run pip3 install picamera
run pip3 install face_recognition
COPY *.py ./
COPY img/* img/
ENTRYPOINT ["python3","main.py"]