FROM python:3.7.6-buster

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY *.py /app/
RUN chmod a+x *.py

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app