FROM archlinux:latest

RUN pacman-key --init
RUN pacman -Syyu --noconfirm
RUN pacman --noconfirm -S git ffmpeg python python-pip megatools
RUN mkdir ./app
WORKDIR ./app/
RUN git clone -b nightly https://github.com/Itz-fork/Mega.nz-Bot.git ./
RUN python -m venv .venv
ENV PATH=".venv/bin:$PATH"
RUN source .venv/bin/activate
RUN python -m pip install --upgrade pip
RUN pip install -U --no-cache-dir -r requirements.txt
CMD ["python", "-m", "bot"]
