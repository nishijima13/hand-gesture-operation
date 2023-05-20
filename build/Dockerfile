FROM ubuntu:20.04

# Set timezone.
ENV TZ Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev v4l-utils libgl1-mesa-dev libglib2.0-0 python3-pyqt5 wget

RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN wget -P /tmp -q https://storage.googleapis.com/mediapipe-tasks/gesture_recognizer/gesture_recognizer.task

WORKDIR /home/workspace
