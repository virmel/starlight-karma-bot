VERSION 0.6
FROM ubuntu:jammy

dockerfile:
  FROM DOCKERFILE .
  SAVE IMAGE starlight

up:
    LOCALLY
    WITH DOCKER --load=+dockerfile
        RUN docker stop starlight || true && docker run --rm --name=starlight -v $(pwd)/data:/data starlight:latest
    END

lint:
  FROM python:3-slim
  RUN pip install black
  COPY src src
  RUN black src
  SAVE ARTIFACT src AS LOCAL src
