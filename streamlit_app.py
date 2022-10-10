import threading
import streamlit as st
from streamlit_webrtc import WebRtcMode
from streamlit_webrtc import webrtc_streamer
from matplotlib import pyplot as plt
import av
import cv2

# st.title("My first Streamlit app")
# st.write("Hello, world2")


# webrtc_streamer(key="sample")



def test1():
    st.write("Running Test1")
    webrtc_streamer(key="sample")

def test2():
    st.write("Running Test2")


    flip = st.checkbox("Flip")
    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")

        flipped = img[::-1,:,:] if flip else img

        return av.VideoFrame.from_ndarray(flipped, format="bgr24")

    webrtc_streamer(key="example", video_frame_callback=video_frame_callback)


def test3():
    st.write("Running Test3")

    show_hist = st.checkbox("Show Histogram")
    
    lock = threading.Lock()
    img_container = {"img": None}

    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        with lock:
            img_container["img"] = img
            # print(img.__dir__,img_container["img"].__dir__)

        return frame


    ctx = webrtc_streamer(key="example", 
        mode=WebRtcMode.SENDRECV,
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        video_frame_callback=video_frame_callback)

    if show_hist:
        fig_place = st.empty()
        fig, ax = plt.subplots(1, 1)

        while ctx.state.playing:
            with lock:
                img = img_container["img"]
            if img is None:
                continue
            # print(len(img),len(img[0]))
            # print(img.__dir__,img_container["img"].__dir__)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ax.cla()
            ax.hist(gray.ravel(), 256, [0, 256])
            fig_place.pyplot(fig)

if __name__=="__main__":

    st.title("webrtc opencv ")
    st.write("Hello,")

    # test1()
    test2()
    # test3()

