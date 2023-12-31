FROM fedora:latest

RUN dnf upgrade -y
RUN dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm -y
RUN dnf install gcc python3-devel  git python3-pip ffmpeg megatools -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
RUN git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot.git /app
RUN pip3 install -U -r requirements.txt
CMD ["python3", "-m", "megadl"]