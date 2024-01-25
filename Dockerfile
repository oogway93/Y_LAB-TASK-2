FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDONUNBUFFERED 1

COPY requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt
COPY . .

CMD ["pytest"]
