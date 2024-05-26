FROM alpine:latest

RUN apk update && apk upgrade
RUN apk add --no-cache gcc python3-dev musl-dev linux-headers git py3-pip ffmpeg
RUN apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ megatools

WORKDIR /app/
COPY . .
RUN python3 -m venv venv
RUN venv/bin/pip install -U -r requirements.txt

CMD ["venv/bin/python3", "-m", "megadl"]