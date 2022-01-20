import time
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def get_frame(self):
        cur = time.time()
        _, frame = self.cap.read()
        
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
        success, img_buffer = cv2.imencode('.jpg', frame, encode_param)
        io_buf = BytesIO(img_buffer)
        io_buf.seek(0)
        data = io_buf.read()
        
        return data

if __name__ == '__main__':
    camera = Camera()
    data = camera.get_frame()

    import cv2

    # 選擇第二隻攝影機
    cap = cv2.VideoCapture(0)

    while(True):
        start = time.time()
        # 從攝影機擷取一張影像
        ret, frame = cap.read()
        
        print(frame.shape)

        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        success, img_buffer = cv2.imencode('.jpg', frame, encode_param)
        io_buf = BytesIO(img_buffer)

        io_buf.seek(0)
        data = io_buf.read()        
        recv_buf = BytesIO(data)
        decode_img = cv2.imdecode(np.frombuffer(recv_buf.getbuffer(), np.uint8), 1)

        # 顯示圖片
        cv2.imshow('frame', decode_img)

        # 若按下 q 鍵則離開迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        print(1/(time.time()-start))

    # 釋放攝影機
    cap.release()

    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()