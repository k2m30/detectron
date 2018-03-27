# nvidia-docker run -it -p 1000:5000 -v ~/detectron/models:/detectron/models -v ~/detectron/k2m30:/detectron/k2m30 detectron:c2-cuda9-cudnn7 /bin/bash
# docker build -t detectron:c2-cuda9-cudnn7 .
# docker exec -it zen_hawking /bin/bash

# Use Caffe2 image as parent image
FROM caffe2/caffe2:snapshot-py2-cuda9.0-cudnn7-ubuntu16.04

RUN mv /usr/local/caffe2 /usr/local/caffe2_build
ENV Caffe2_DIR /usr/local/caffe2_build

ENV PYTHONPATH /usr/local/caffe2_build:${PYTHONPATH}
ENV LD_LIBRARY_PATH /usr/local/caffe2_build/lib:${LD_LIBRARY_PATH}

# Install Python dependencies
RUN pip install numpy>=1.13 pyyaml>=3.12 matplotlib opencv-python>=3.2 setuptools Cython mock scipy flask

# Install the COCO API
RUN git clone https://github.com/cocodataset/cocoapi.git /cocoapi
WORKDIR /cocoapi/PythonAPI
RUN make install

# Clone the Detectron repository
RUN ls
RUN git clone https://github.com/facebookresearch/detectron /detectron

# Set up Python modules
WORKDIR /detectron/lib
RUN make

# Build custom ops
RUN make ops

WORKDIR /detectron
RUN apt update && apt install -y wget iputils-ping iproute2

WORKDIR root
RUN mkdir /detectron/tools/templates
RUN ln -s /detectron/k2m30/webcam/templates/index.html /detectron/tools/templates/index.html
RUN ln -s /detectron/k2m30/webcam/e2e_mask_rcnn_R-101-FPN_2x.yaml /detectron/e2e_mask_rcnn_R-101-FPN_2x.yaml
RUN ln -s /detectron/k2m30/webcam/infer_simple_k2m30.py /detectron/tools/infer_simple_k2m30.py
RUN ln -s /detectron/k2m30/webcam/vis_k2m30.py /detectron/lib/utils/vis_k2m30.py
# Go to Detectron root
WORKDIR /detectron