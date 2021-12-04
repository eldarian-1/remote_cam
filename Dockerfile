FROM python:3.6

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python ./server/manage.py makemigrations main
RUN python ./server/manage.py migrate

EXPOSE 8000

CMD ["python", "./server/manage.py", "runserver", "0.0.0.0:8000"]