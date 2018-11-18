#!/bin/bash
# Restart the raspberry pi camera stream

# On Windows the command to run is:
# gst-launch-1.0 udpsrc port=<ANYPORT> ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink

# Change <WINDOWSIPHERE> to the gst-launch-1.0 server ip and port=<ANYPORT> to the gst-launch-1.0 server port
#raspivid -t 0 -n -h 720 -w 1280 -fps 60 -b 3000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse config-interval=1 ! rtph264pay ! udpsink host=<WINDOWSIPHERE> port=<ANYPORT>

# CURRENTLY FOR TESTING PURPOSES
echo "testing"
