#!/bin/bash

set -xv

mkdir -p /data
if [ ! -f /data/karma.json ]; then
  echo "{}" > /data/karma.json
fi
if [ ! -f /data/points.json ]; then
  echo "{}" > /data/points.json
fi

pipenv run python src/main.py
