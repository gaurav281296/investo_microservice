FROM python:3.9.2-slim-buster
ENV PYTHONUNBUFFERED 1
ADD . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install --reinstall -y libpq-dev
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["bash", "start_server.sh"]