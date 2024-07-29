FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN rm -rf /root/.cache/pip
WORKDIR /app
COPY requirements.txt /Core/requirements.txt

RUN pip install --upgrade pip
RUN python3 -m pip install -r /Core/requirements.txt
