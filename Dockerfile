# docker build --progress plain --network=host -f Dockerfile -t sam:test .
#--build-arg http_proxy=http://127.0.0.1:11000 --build-arg https_proxy=http://127.0.0.1:11000 

FROM nvcr.io/nvidia/cuda:11.7.1-devel-ubuntu22.04

ENV NVIDIA_DRIVER_CAPABILITIES video,compute,utility

ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ 

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update

RUN apt-get purge -y --auto-remove python3 && \
    apt-get install -y python3.10 python3.10-dev python3.10-distutils wget && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

# for opencv-python
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2

RUN apt-get update && apt-get install -y git python3-tk  wget

RUN pip install git+https://github.com/facebookresearch/segment-anything.git

RUN pip install opencv-python pycocotools matplotlib onnxruntime onnx gradio

WORKDIR /usr/app

COPY . .
# WORKDIR /weights

# COPY sam_vit_h_4b8939.pth /weights

