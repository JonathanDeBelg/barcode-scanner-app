import streamlit as st
import pandas as pd
import numpy as np
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from streamlit_webrtc import webrtc_streamer
import av

from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

st.title('Barcode test app')

class VideoProcessor:
    def recv(self, image):
        img = image.to_ndarray(format="bgr24")
        
        gray_img = cv2.cvtColor(img,0) 
        barcode = decode(gray_img)

        for obj in barcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            string = "Data: " + str(barcodeData) + " | Type: " + str(barcodeType)
            
            cv2.putText(img, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255), 2)

            print("Barcode: "+barcodeData +" | Type: "+barcodeType)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
        

webrtc_streamer(
    key="example", 
    video_processor_factory=VideoProcessor,
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={"video": True, "audio": False},
)