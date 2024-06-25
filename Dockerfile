# docker build --progress plain --network=host -f Dockerfile -t registry.light-field.tech/citygen/sam:test .
#--build-arg http_proxy=http://127.0.0.1:11000 --build-arg https_proxy=http://127.0.0.1:11000 

FROM nvcr.io/nvidia/cuda:11.7.1-devel-ubuntu22.04

ENV NVIDIA_DRIVER_CAPABILITIES all

ENV TZ=Asia/Shanghai

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ 

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse" > /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse" >> /etc/apt/sources.list && \
    echo "deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse" >> /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get purge -y --auto-remove python3 && \
    apt-get install -y python3.10 python3.10-dev python3.10-distutils wget && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    pip install --upgrade pip pysocks

RUN apt-get update && \
    apt-get install -y  openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:root' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    pip install --no-cache-dir  -i https://pypi.tuna.tsinghua.edu.cn/simple jupyterlab   

# for opencv-python
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2

RUN apt-get update && apt-get install -y git python3-tk  wget

RUN pip install git+https://github.com/facebookresearch/segment-anything.git

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python pycocotools matplotlib onnxruntime onnx gradio

RUN pip install "numpy <2" --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple



# WORKDIR /usr/app

# COPY . .

# WORKDIR /weights

# COPY sam_vit_h_4b8939.pth /weights

