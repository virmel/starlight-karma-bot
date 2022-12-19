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

test:
  FROM +dockerfile
  RUN pipenv run pytest

lint.black:
  FROM python:3-slim
  RUN pip install black
  COPY src src
  RUN black src
  SAVE ARTIFACT src AS LOCAL src

lint.pylint:
  FROM python:3-slim
  RUN pip install pylint
  COPY src src
  RUN pylint -d C0301,C0116,C0115,C0114,E0401,R0903 src
  SAVE ARTIFACT src AS LOCAL src
