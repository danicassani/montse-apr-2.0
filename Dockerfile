FROM python:3.10.6
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y
RUN apt-get install -y ffmpeg git curl
COPY requirements.txt .
COPY montse.py .

COPY manage.py .
COPY settings.py .
COPY db/ .
COPY .env .
COPY utils/ ./utils/

RUN ls -la
RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "montse.py"]