FROM archlinux:latest

RUN pacman -Syyu
RUN pacman -S git ffmpeg python python-pip megatools
RUN mkdir app
WORKDIR /app
RUN git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot.git
RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -U -r requirements.txt
CMD ["python", "-m", "bot"]