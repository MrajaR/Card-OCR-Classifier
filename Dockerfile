FROM python:3.8

COPY . /app
WORKDIR /app

ENV PYHTONUNBUFFERED=1

COPY ./app/detection_model/card_classifier.h5 app/detection_model/card_classifier.h5

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app/app_2.py"]