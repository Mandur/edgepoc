import face_recognition
import os
import cv2
import json
from sender import Sender

def do_face_recognition():
    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

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


    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

   # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]


    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
    # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            #put processing here
        face_names.append(name)
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return face_names[0]


def main():
    detection_index=0
    # These variables are set by the IoT Edge Agent
    CONNECTION_STRING = os.getenv('EdgeHubConnectionString', "<no edge aivalable>")
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
