import sys
import time
import cv2
from kafka import KafkaProducer

topic = "distributed-video1"


def publish_video(video_file):
    # Start KafkaProducer
    producer = KafkaProducer(
        bootstrap_servers = 'localhost:9092'
    )

    # Video File Operations
    video = cv2.VideoCapture(video_file)

    print("publishing video.....started")

    while(video.isOpened()):
        success, frame = video.read()

        if not success:
            print("bad file read")
            break

        ret, buffer = cv2.imencode('.jpg', frame)

        producer.send(topic, buffer.tobytes())

        time.sleep(0.2)

    video.release()
    print("publishing video.....completed")


def publish_camera():
    '''
    Publish Camera 
    '''
    producer = KafkaProducer(
        bootstrap_servers = 'localhost:9092'
    )

    camera = cv2.VideoCapture(1)

    try:
        while(True):
            success, frame = camera.read()

            flipped_frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', flipped_frame)

            producer.send(topic, buffer.tobytes())

            time.sleep(0.2)

    except:
        print("exiting code.....")
        sys.exit(1)

    camera.release()


if __name__ == "__main__":

    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print("publishing feed!")
        publish_camera()

    pass
