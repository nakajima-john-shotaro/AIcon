#!/bin/bash

PYTORCH_VERSION="1.7.1"
CUDA_VERSION="11.0"
CUDNN_VERSION="8"
IMAGE_FLAVOR="devel"
OPENCV_VERSION="4.4.0.46"
BUILD_DIR=$(dirname $(readlink -f $0))/src
USER_ID=$(id -u)

declare -ar USABLE_PYTORCH_VERSIONS=("1.0", "1.0.1", "1.1.0", "1.2", "1.3", "1.4", "1.5", "1.5.1", "1.6.0", "1.7.0", "1.7.1")
declare -ar USABLE_CUDA_VERSIONS=("10.0", "10.1", "11.0")
declare -ar USABLE_CUDNN_VERSIONS=("7", "8")
declare -ar USABLE_FLAVORS=("runtime", "devel")
declare -ar USABLE_CV_VERSIONS=("3.4.8.29", "3.4.9.31", "3.4.9.33", "3.4.10.35", "3.4.10.37", "3.4.11.39", "3.4.11.41", "3.4.11.43", "3.4.11.45", "3.4.13.47", "4.1.2.30", "4.2.0.32", "4.2.0.34", "4.3.0.36", "4.3.0.38", "4.4.0.40", "4.4.0.42", "4.4.0.44", "4.4.0.46", "4.5.1.48", "off")

function usage_exit {
  cat <<_EOS_ 1>&2
  Usage: $PROG_NAME [OPTIONS...]
  OPTIONS:
    -h,                show this help message and exit
    -p,  VERSION       pytorch version (default: 1.7.1)
    -c,  VERSION       cuda version (default: 11.0)
    -d,  VERSION       cudnn version (default: 8)
    -f,  FLAVOR        docker image flavor (default: devel)
    -o, {VERSION|off}  opencv version (default: 4.4.0.46)
_EOS_
    exit 1
}

while getopts hp:c:d:f:o: OPT
do
  case $OPT in
    "h" ) FLG_HELP="TRUE" ;;
    "p" ) FLG_PYTORCH_VERSION="TRUE" ; PYTORCH_VERSION="$OPTARG" ;;
    "c" ) FLG_CUDA_VERSION="TRUE" ;    CUDA_VERSION="$OPTARG" ;;
    "d" ) FLG_CUDNN_VERSION="TRUE" ;   CUDNN_VERSION="$OPTARG" ;;
    "f" ) FLG_IMAGE_FLAVOR="TRUE" ;    IMAGE_FLAVOR="$OPTARG" ;;
    "o" ) FLG_OPENCV_VERSION="TRUE" ;  OPENCV_VERSION="$OPTARG" ;;
      * ) usage_exit
  esac
done

if [ "$FLG_HELP" = "TRUE" ]; then
  usage_exit
fi

if [ "$FLG_PYTORCH_VERSION" = "TRUE" ]; then
  local _e="false"
  for v in "${USABLE_PYTORCH_VERSIONS[@]}"; do
    if [[ ${PYTORCH_VERSION} == ${v} ]]; then
        _e="true"
    fi
  done
  if [[ ${_e} == "false" ]]; then
    echo "E: invalid parameter: ${PYTORCH_VERSION}"
    echo "available pytorch versions: ${USABLE_PYTORCH_VERSIONS[@]}"
    exit 1
  fi
fi

if [ "$FLG_CUDA_VERSION" = "TRUE" ]; then
  local _e="false"
  for v in "${USABLE_CUDA_VERSIONS[@]}"; do
    if [[ ${CUDA_VERSION} == ${v} ]]; then
        _e="true"
    fi
  done
  if [[ ${_e} == "false" ]]; then
    echo "E: invalid parameter: ${CUDA_VERSION}"
    echo "available cuda versions: ${USABLE_CUDA_VERSIONS[@]}"
    exit 1
  fi
fi

if [ "$FLG_CUDNN_VERSION" = "TRUE" ]; then
  local _e="false"
  for v in "${USABLE_CUDNN_VERSIONS[@]}"; do
    if [[ ${CUDNN_VERSION} == ${v} ]]; then
        _e="true"
    fi
  done
  if [[ ${_e} == "false" ]]; then
    echo "E: invalid parameter: ${CUDNN_VERSION}"
    echo "available cudnn versions: ${USABLE_CUDNN_VERSIONS[@]}"
    exit 1
  fi
fi

if [ "$FLG_IMAGE_FLAVOR" = "TRUE" ]; then
  local _e="false"
  for v in "${USABLE_FLAVORS[@]}"; do
    if [[ ${IMAGE_FLAVOR} == ${v} ]]; then
        _e="true"
    fi
  done
  if [[ ${_e} == "false" ]]; then
    echo "E: invalid parameter: ${IMAGE_FLAVOR}"
    echo "available image flavors: ${USABLE_FLAVORS[@]}"
    exit 1
  fi
fi

if [ "$FLG_OPENCV_VERSION" = "TRUE" ]; then
  local _e="false"
  for v in "${USABLE_CV_VERSIONS[@]}"; do
    if [[ ${OPENCV_VERSION} == ${v} ]]; then
        _e="true"
    fi
  done
  if [[ ${_e} == "false" ]]; then
    echo "E: invalid parameter: ${OPENCV_VERSION}"
    echo "available opencv versions: ${USABLE_CV_VERSIONS[@]}"
    exit 1
  fi
fi

PYTORCH_IMAGE_NAME="pytorch:${PYTORCH_VERSION}-cuda${CUDA_VERSION}-cudnn${CUDNN_VERSION}-${IMAGE_FLAVOR}-opencv${OPENCV_VERSION}"

docker build \
  -t ${PYTORCH_IMAGE_NAME} \
  -f ${BUILD_DIR}/Dockerfile \
  --build-arg PYTORCH_VERSION=${PYTORCH_VERSION} \
  --build-arg CUDA_VERSION=${CUDA_VERSION} \
  --build-arg CUDNN_VERSION=${CUDNN_VERSION} \
  --build-arg IMAGE_FLAVOR=${IMAGE_FLAVOR} \
  ${BUILD_DIR}