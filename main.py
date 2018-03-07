import os
import json
import face_recognition
import picamera
import numpy as np
# IOT code
from sender import Sender


def setup():
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)

    # Load a sample picture and learn how to recognize it.
    lars = face_recognition.load_image_file("img/lars_hulstaert.jpg")
    lars_face_encodings = face_recognition.face_encodings(lars)[0]

    mikhail = face_recognition.load_image_file("img/mikhail_chatillon.jpg")
    mikhail_face_encodings = face_recognition.face_encodings(mikhail)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        mikhail_face_encodings, lars_face_encodings]
    known_face_names = [
        "Mikhail", "Lars"
    ]
    print('Setup the face recognition for the following people:')
    for name in known_face_names:
        print(name)
    return camera, known_face_encodings, known_face_names

def do_face_recognition(camera, known_face_encodings, known_face_names):
    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Initialize some variables
    face_locations = []
    face_encodings = []
    output = np.empty((480, 640, 3), dtype=np.uint8)

    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    if(len(face_locations)==0):
        return ""
    face_encodings = face_recognition.face_encodings(output, face_locations)
    name = "Unknown Person"
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        for idx, known_encoding in enumerate(known_face_encodings):
            match = face_recognition.compare_faces([known_encoding], face_encoding)
            if match[0]:
                name = known_face_names[idx]
                print("I see someone named {}!".format(name)) 
    return name
    


def main():
    detection_index=0
    # These variables are set by the IoT Edge Agent
    CONNECTION_STRING = os.getenv('EdgeHubConnectionString')
    CA_CERTIFICATE = os.getenv('EdgeModuleCACertificateFile', False)
    sender = Sender(CONNECTION_STRING, CA_CERTIFICATE)
    print("connected to "+CONNECTION_STRING)
    print('Setting up face recognition module')
    camera, known_face_encodings, known_face_names = setup()
    while True:
        recognized_person=do_face_recognition(camera, known_face_encodings, known_face_names)
        if recognized_person != "":
            print(recognized_person)
            if sender:
                msg_properties = {
                    'detection_index': str(detection_index)
                }
            json_formatted = json.dumps({"face":recognized_person})
            sender.send_event_to_output(json_formatted, msg_properties, detection_index)

main()

