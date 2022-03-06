FROM python:3.7-alpine

WORKDIR /app/api

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

CMD [ "python", "api.py" ,"--host=0.0.0.0"]