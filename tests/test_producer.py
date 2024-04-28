import cv2
import pytest
from unittest.mock import patch, MagicMock
from publish import publish_video, publish_camera


@pytest.fixture
def mocked_producer():
    return MagicMock()


@pytest.fixture
def mocked_video_capture():
    return MagicMock()


@patch('publish.cv2.VideoCapture')
@patch('publish.KafkaProducer')
def test_publish_video(mocked_kafka_producer, mocked_video_capture):
    mocked_producer_instance = MagicMock()
    mocked_kafka_producer.return_value = mocked_producer_instance

    # Simulate video file
    mocked_video_capture_instance = MagicMock()
    mocked_video_capture_instance.isOpened.return_value = True
    mocked_video_capture_instance.read.side_effect = [
        (True, cv2.imread('test_image.jpg')),
        (True, cv2.imread('test_image.jpg')),
        (False, None)  # End of file
    ]
    mocked_video_capture.return_value = mocked_video_capture_instance

    publish_video('test_video.mp4')

    # Check if KafkaProducer methods were called
    assert mocked_producer_instance.send.call_count == 2

    # Check if VideoCapture methods were called
    assert mocked_video_capture_instance.read.call_count == 3


@patch('publish.cv2.VideoCapture')
@patch('publish.KafkaProducer')
def test_publish_camera(mocked_kafka_producer, mocked_video_capture):
    mocked_producer_instance = MagicMock()
    mocked_kafka_producer.return_value = mocked_producer_instance

    # Simulate camera feed
    mocked_video_capture_instance = MagicMock()
    mocked_video_capture_instance.read.return_value = (True, cv2.imread('test_image.jpg'))
    mocked_video_capture.return_value = mocked_video_capture_instance

    with pytest.raises(SystemExit):
        publish_camera()

    # Check if KafkaProducer methods were called
    assert mocked_producer_instance.send.call_count >= 1

    # Check if VideoCapture methods were called
    assert mocked_video_capture_instance.read.call_count >= 1

