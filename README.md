# Magic_Streaming

## How to Run

Before Running Code

```bash
pip install -r requirements.txt  # install
```

Server side

```bash
cd src
python3 main_server.py --ip 0.0.0.0
```

Client side

```bash
cd src
python3 Gui.py --ip <rtsp server ip>
```

Example:

Server side

```bash
cd src
python3 main_server.py --ip 127.0.0.1 --port  8888
```

Client side

```bash
cd src
python3 Gui.py --ip 127.0.0.1 --port  8888
```

Reference:
YOLOv5: https://github.com/ultralytics/yolov5
rtsp-rtp-stream: https://github.com/gabrieljablonski/rtsp-rtp-stream
