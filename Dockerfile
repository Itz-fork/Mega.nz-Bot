FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git python3-pip ffmpeg -y
RUN apt -qq install -y --no-install-recommends megatools
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
RUN git clone https://github.com/Itz-fork/Mega.nz-Bot.git /app
RUN pip3 install -U -r requirements.txt
CMD bash startup.sh
