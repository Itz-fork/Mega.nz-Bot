FROM fedora:latest

RUN dnf upgrade -y
RUN dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm -y
RUN dnf install git python3-pip ffmpeg megatools -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
RUN git clone https://github.com/Itz-fork/Mega.nz-Bot.git /app
RUN pip3 install -U -r requirements.txt
CMD [ "bash", "startup.sh" ]
