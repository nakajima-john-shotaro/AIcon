ARG PYTORCH_VERSION="1.7.1"
ARG CUDA_VERSION="11.0"
ARG CUDNN_VERSION="8"
ARG IMAGE_FLAVOR="devel"

FROM pytorch/pytorch:${PYTORCH_VERSION}-cuda${CUDA_VERSION}-cudnn${CUDNN_VERSION}-${IMAGE_FLAVOR}

RUN sed -i 's@archive.ubuntu.com@ftp.jaist.ac.jp/pub/Linux@g' /etc/apt/sources.list

LABEL maintainer="tasakilab"

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /home/pytorch 

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        gosu \
        build-essential \
        pkg-config \
        git \
        curl \
        less \
        emacs \
        vim \
        tmux \
        bash-completion \
        command-not-found \
        software-properties-common \
        xdg-user-dirs \
        xsel \
        dirmngr \
        gpg-agent \
        mesa-utils \
        libglu1-mesa-dev \
        libgles2-mesa-dev \
        freeglut3-dev \
        libcanberra-gtk-module \
        libcanberra-gtk3-module \
        python3-pip \
        python3-dev \
        gfortran \
        libopenblas-dev \
        libhdf5-serial-dev \
        hdf5-tools \
        libhdf5-dev \
        zlib1g-dev \
        zip \
        libpng-dev \
        libfreetype6-dev \
        libopenmpi-dev \
        libopenexr-dev \
        openexr \
        zlib1g-dev \
        libjpeg8-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "PYTHONIOENCODING=utf-8" >> /root/.bashrc && \
    echo "TF_CPP_MIN_LOG_LEVEL=2" >> /root/.bashrc && \
    echo "export PS1='\[\033[01;32m\]pytorch@docker\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> /root/.bashrc

RUN pip3 install \
        setuptools \
        Cython \
        wheel --verbose
RUN pip3 install \
        numpy --verbose
RUN HDF5_DIR=/usr/lib/aarch64-linux-gnu/hdf5/serial/ \
    pip3 install \
        h5py==2.9.0 --verbose
RUN pip3 install \
        future==0.17.1 \
        mock==3.0.5 \
        gast==0.2.2 \
        futures \
        protobuf \
        pybind11 --verbose
RUN pip3 install \
        six \
        cycler \
        kiwisolver \
        pyparsing \
        python-dateutil \
        scikit-image==0.16.2 --verbose
RUN pip3 install --no-dependencies \
        matplotlib --verbose \
        seaborn --verbose \
        pandas --verbose
RUN pip3 install \
        scikit-learn --verbose \
        pyyaml --verbose
RUN pip3 install \
        tensorboard --verbose \
        torchsummary --verbose
RUN pip3 install \
        opencv-contrib-python==4.4.0.46 --verbose \
        OpenEXR
RUN pip3 install \
        visdom --verbose \
        dominate
        
WORKDIR /home/pytorch
