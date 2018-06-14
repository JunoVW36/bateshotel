FROM python:3.6.4
ENV PYTHONUNBUFFERED 1

# Upgrade pip before installing packages
RUN pip install --upgrade --no-cache-dir pip

COPY requirements.txt /home/docker/code/
RUN pip install -r /home/docker/code/requirements.txt

