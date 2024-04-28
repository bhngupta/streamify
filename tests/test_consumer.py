from flask import Response
from unittest.mock import MagicMock, patch
import pytest
from consumer import app, get_video_stream

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch('consumer.KafkaConsumer')
def test_video_feed_route(mocked_kafka_consumer, client):
    # Mock KafkaConsumer
    mocked_consumer_instance = MagicMock()
    mocked_kafka_consumer.return_value = mocked_consumer_instance

    # Simulate Kafka messages
    mocked_consumer_instance.__iter__.return_value = iter([
        b'fake_image_data_1',
        b'fake_image_data_2',
        b'fake_image_data_3'
    ])

    response = client.get('/video_feed')

    # Check if response is a multipart response
    assert response.content_type == 'multipart/x-mixed-replace; boundary=frame'

    # Check if response contains expected data
    expected_data = b'--frame\r\nContent-Type: image/jpg\r\n\r\nfake_image_data_1\r\n\r\n'
    assert expected_data in response.data

    # Check if KafkaConsumer methods were called
    assert mocked_consumer_instance.__iter__.called

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_get_video_stream():
    # Mock KafkaConsumer
    mocked_consumer_instance = MagicMock()

    # Simulate Kafka messages
    mocked_consumer_instance.__iter__.return_value = iter([
        b'fake_image_data_1',
        b'fake_image_data_2',
        b'fake_image_data_3'
    ])

    with patch('consumer.consumer', new=mocked_consumer_instance):
        generator = get_video_stream()

        # Check if generator yields expected data
        assert next(generator) == b'--frame\r\nContent-Type: image/jpg\r\n\r\nfake_image_data_1\r\n\r\n'
        assert next(generator) == b'--frame\r\nContent-Type: image/jpg\r\n\r\nfake_image_data_2\r\n\r\n'
        assert next(generator) == b'--frame\r\nContent-Type: image/jpg\r\n\r\nfake_image_data_3\r\n\r\n'

        # Test stopping iteration
        with pytest.raises(StopIteration):
            next(generator)

