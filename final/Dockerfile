FROM python:3-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY alert.schema.json .
COPY ammute.py .

CMD [ "python", "./ammute.py" ]
