import os
import json
from sender import Sender
import face_recognition
import picamera
import numpy as np

def do_face_recognition():
    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    output = np.empty((240, 320, 3), dtype=np.uint8)

    # Load a sample picture and learn how to recognize it.
    mik = face_recognition.load_image_file("img/me.jpg")
    mik_face_encodings = face_recognition.face_encodings(mik)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        mik_face_encodings]
    known_face_names = [
        "Mikhail"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []


    print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="rgb")
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)
         # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            name = "<Unknown Person>"
            if match[0]:
                name = "Barack Obama"
            print("I see someone named {}!".format(name))
            return face_names[0]
    return null
    


def main():
    detection_index=0
    # These variables are set by the IoT Edge Agent
    CONNECTION_STRING = os.getenv('EdgeHubConnectionString')
    CA_CERTIFICATE = os.getenv('EdgeModuleCACertificateFile', False)
    sender = Sender(CONNECTION_STRING, CA_CERTIFICATE)
    print("connected to "+CONNECTION_STRING)
    while True:
        recognized_person=do_face_recognition()
        print(recognized_person)
        if sender:
            msg_properties = {
                'detection_index': str(detection_index)
            }
        json_formatted = json.dumps(recognized_person)
        sender.send_event_to_output('detectionOutput', json_formatted, msg_properties, detection_index)

if __name__ == "__main__":
    main()
