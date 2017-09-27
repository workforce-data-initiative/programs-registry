
FROM python:alpine
WORKDIR /app
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD . .
CMD [ "python3", "app.py" ]
