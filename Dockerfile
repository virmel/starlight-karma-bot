FROM python:3-slim
RUN pip install pipenv

RUN mkdir -p /app
WORKDIR /app

COPY Pipfile Pipfile.lock .
RUN pipenv install

COPY *.env .
COPY src src
COPY assets assets
COPY --chmod=0755 start.sh .

EXPOSE 8080

CMD ["./start.sh"]
