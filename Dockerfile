FROM alpine:latest

RUN apk update && apk upgrade
RUN apk add --no-cache gcc python3-dev git py3-pip ffmpeg megatools
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
RUN git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot.git /app
RUN pip3 install -U -r requirements.txt
CMD ["python3", "-m", "megadl"]
