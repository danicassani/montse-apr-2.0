FROM python:3.10.6
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install -y ffmpeg git curl

COPY . ./


RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "montse.py"]