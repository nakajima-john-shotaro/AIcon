#!/bin/bash

CONTAINER_NAME="pytorch"
CONTAINER_ID=""

PROG_NAME=$(basename $0)

function usage_exit {
  cat <<_EOS_ 1>&2
  Usage: $PROG_NAME [OPTIONS...]
  OPTIONS:
    -h,             show this help message and exit
    -n,  NAME/ID    container name or id (default: pytorch)
_EOS_
    exit 1
}

while getopts hn: OPT
do
  case $OPT in
    "h" ) FLG_HELP="TRUE" ;;
    "n" ) FLG_CONTAINER_NAME="TRUE" ; CONTAINER_NAME="$OPTARG" ;;
      * ) usage_exit
  esac
done

if [ "$FLG_HELP" = "TRUE" ]; then
  usage_exit
fi

CONTAINER_ID=$(docker ps | grep "${CONTAINER_NAME}")
CONTAINER_NUMS=$(docker ps | grep "${CONTAINER_NAME}" | wc -l)

if [[ ${CONTAINER_NUMS} == "0" ]]; then
    echo "E: cannot find the running container named ${CONTAINER_NAME}"
    echo ""
    docker ps
    echo ""
    usage_exit
elif [[ ${CONTAINER_NUMS} != "1" ]]; then
    echo "E: There are multiple containers running. Identify the container."
    echo ""
    docker ps
    echo ""
    usage_exit
fi

CONTAINER_ID=${CONTAINER_ID:0:12}

clear

printf "\033[01;31m\n"
printf " ________          ________                      ______ \n";
printf " ___  __ \_____  _____  __/______ __________________  /_ \n";
printf " __  /_/ /__  / / /__  /   _  __ \__  ___/_  ___/__  __ \ \n";
printf " _  ____/ _  /_/ / _  /    / /_/ /_  /    / /__  _  / / / \n";
printf " /_/      _\__, /  /_/     \____/ /_/     \___/  /_/ /_/ \n";
printf "          /____/ ";
printf "\n"
printf "\n"
printf "\033[00m\033[33m\n"
printf "WARNING: You are running this container as root, which can cause new files in\n"
printf "mounted volumes to be created as the root user on your host machine.\n"
printf "\033[00m\n"

docker exec -it ${CONTAINER_ID} /bin/bash