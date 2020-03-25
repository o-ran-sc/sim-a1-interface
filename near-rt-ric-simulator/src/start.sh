#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Expected folder name of simulator."
    echo "The container shall be started with env variable 'A1_VERSION' set to the folder name of the A1 version to use."
    echo "Exiting...."
    exit 1
fi
echo "Version folder for simulator: "$1

#Set path to open api
export APIPATH=$PWD/api/$1
echo "APIPATH set to: "$APIPATH

cd src

#Include common module(s)
export PYTHONPATH=$PWD/common
echo "PYTHONPATH set to: "$PYTHONPATH

cd $1

echo "Path to main.py: "$PWD
python -u main.py
