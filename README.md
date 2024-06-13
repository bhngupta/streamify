# streamify
Streamify is a simple Distributed Video Streaming Platform written in Python and uses Kafka

Using Apache Kafka as the messaging broker and Flask as the web server. The codebase consists of two main components: a producer that captures video frames and publishes them to a Kafka topic, and a consumer that consumes these frames and streams them to a web client.

## Features

- Streams video from a camera or a video file to a web client.
- Uses Apache Kafka for messaging, providing scalability and fault tolerance.
- Utilizes Flask, a lightweight web framework, for serving the video stream to clients.
- Supports real-time video streaming with minimal latency.

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/distributed-video-streaming
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Make sure you have Apache Kafka installed and running on your system. You can download Kafka from the [official website](https://kafka.apache.org/downloads) and follow the instructions for setup.

## Usage

### Running the Producer

To publish video frames to Kafka, run the producer script `producer.py`. You can specify a video file as an argument or omit it to capture video from a camera.

```bash
python producer.py <path to video file(optional)>
```

### Running the Consumer

To consume video frames from Kafka and stream them to a web client, run the consumer script consumer.py. This will start a Flask server that serves the video stream.

```bash
python consumer.py
```

### Accessing the Video Stream

Once the consumer is running, you can access the video stream by navigating to http://localhost:8000/video_feed in your web browser.

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to the developers of Apache Kafka, Flask, and OpenCV for providing the tools and libraries that make this project possible.
